// SPDX-License-Identifier: BUSL-1.1
// SPDX-FileCopyrightText: 2024 Kiln <contact@kiln.fi>
//
// ██╗  ██╗██╗██╗     ███╗   ██╗
// ██║ ██╔╝██║██║     ████╗  ██║
// █████╔╝ ██║██║     ██╔██╗ ██║
// ██╔═██╗ ██║██║     ██║╚██╗██║
// ██║  ██╗██║███████╗██║ ╚████║
// ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═══╝
//
pragma solidity 0.8.22;

import {IERC20Metadata} from "@openzeppelin/interfaces/IERC20Metadata.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

import {AddressNotContract, NothingToClaim} from "../Errors.sol";
import {IConnector, IERC20} from "../interfaces/IConnector.sol";

/// @dev Partial IPool interface.
interface Aave {
    function supply(address asset, uint256 amount, address onBehalfOf, uint16 referralCode) external;
    function withdraw(address asset, uint256 amount, address to) external returns (uint256);
}

/// @dev Partial IPoolDataProvider interface.
interface PoolDataProvider {
    function getReserveTokensAddresses(address asset) external view returns (address, address, address);
    function getReserveConfigurationData(address asset)
        external
        view
        returns (
            uint256 decimals,
            uint256 ltv,
            uint256 liquidationThreshold,
            uint256 liquidationBonus,
            uint256 reserveFactor,
            bool usageAsCollateralEnabled,
            bool borrowingEnabled,
            bool stableBorrowRateEnabled,
            bool isActive,
            bool isFrozen
        );
    function getReserveData(address asset)
        external
        view
        returns (
            uint256 unbacked,
            uint256 accruedToTreasuryScaled,
            uint256 totalAToken,
            uint256 totalStableDebt,
            uint256 totalVariableDebt,
            uint256 liquidityRate,
            uint256 variableBorrowRate,
            uint256 stableBorrowRate,
            uint256 averageStableBorrowRate,
            uint256 liquidityIndex,
            uint256 variableBorrowIndex,
            uint40 lastUpdateTimestamp
        );
    function getReserveCaps(address asset) external view returns (uint256 borrowCap, uint256 supplyCap);
    function getPaused(address asset) external view returns (bool);
}

/// @title Aave V3 Connector.
contract AaveV3Connector is IConnector {
    using SafeERC20 for IERC20;

    /// @notice Aave V3 lending pool address.
    Aave public immutable aave;

    /// @notice Aave V3 pool data provider address.
    PoolDataProvider public immutable poolDataProvider;

    constructor(address _aave, address _poolDataProvider) {
        if (_aave.code.length == 0) revert AddressNotContract(_aave);
        if (_poolDataProvider.code.length == 0) revert AddressNotContract(_poolDataProvider);
        aave = Aave(_aave);
        poolDataProvider = PoolDataProvider(_poolDataProvider);
    }

    /// @inheritdoc IConnector
    function totalAssets(IERC20 asset) external view returns (uint256) {
        (address _aToken,,) = poolDataProvider.getReserveTokensAddresses(address(asset));
        return IERC20(_aToken).balanceOf(msg.sender);
    }

    /// @inheritdoc IConnector
    function deposit(IERC20 asset, uint256 amount) external {
        asset.forceApprove(address(aave), amount);
        aave.supply(address(asset), amount, address(this), 0);
    }

    /// @inheritdoc IConnector
    function withdraw(IERC20 asset, uint256 amount) external {
        aave.withdraw(address(asset), amount, address(this));
    }

    /// @inheritdoc IConnector
    function claim(IERC20, IERC20, bytes calldata) external pure override {
        revert NothingToClaim();
    }

    /// @inheritdoc IConnector
    function maxDeposit(IERC20 asset) external view override returns (uint256) {
        (,,,,,,,, bool _isActive, bool _isFrozen) = poolDataProvider.getReserveConfigurationData(address(asset));
        bool _isPaused = poolDataProvider.getPaused(address(asset));
        if (!_isActive || _isFrozen || _isPaused) {
            return 0;
        }

        (, uint256 _rawSupplyCap) = poolDataProvider.getReserveCaps(address(asset));

        // If not capped
        if (_rawSupplyCap == 0) {
            return type(uint256).max - 1;
        }

        // We need to scale the supply cap to the asset decimals
        uint256 _supplyCap = _rawSupplyCap * 10 ** IERC20Metadata(address(asset)).decimals();

        (, uint256 _accruedToTreasuryScaled, uint256 _totalAToken,,,,,,,,,) =
            poolDataProvider.getReserveData(address(asset));

        // If supply cap already reached
        if (_totalAToken + _accruedToTreasuryScaled >= _supplyCap) {
            return 0;
        }

        return _supplyCap - (_totalAToken + _accruedToTreasuryScaled);
    }

    /// @inheritdoc IConnector
    function maxWithdraw(IERC20 asset) external view override returns (uint256) {
        (,,,,,,,, bool _isActive,) = poolDataProvider.getReserveConfigurationData(address(asset));
        bool _isPaused = poolDataProvider.getPaused(address(asset));
        if (!_isActive || _isPaused) {
            return 0;
        }

        (address _aToken,,) = poolDataProvider.getReserveTokensAddresses(address(asset));
        return asset.balanceOf(address(_aToken));
    }
}
