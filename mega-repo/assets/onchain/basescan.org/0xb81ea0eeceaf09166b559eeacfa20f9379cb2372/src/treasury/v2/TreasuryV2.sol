// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {ITreasuryV2, NATIVE_TOKEN} from "./interfaces/ITreasuryV2.sol";
import {AccessControlUpgradeable} from "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";
import {Ownable2StepUpgradeable} from "@openzeppelin/contracts-upgradeable/access/Ownable2StepUpgradeable.sol";
import {PausableUpgradeable} from "@openzeppelin/contracts-upgradeable/utils/PausableUpgradeable.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {Initializable} from "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import {UUPSUpgradeable} from "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";

/// @custom:oz-upgrades-from Treasury
contract TreasuryV2 is
    Initializable,
    UUPSUpgradeable,
    ITreasuryV2,
    Ownable2StepUpgradeable,
    PausableUpgradeable,
    AccessControlUpgradeable
{
    using SafeERC20 for IERC20;

    /// @custom:storage-location erc7201:treasury.storage
    struct TreasuryStorage {
        IERC20 icnToken;
        address reserveContract;
    }

    // keccak256(abi.encode(uint256(keccak256("treasury.storage")) - 1)) & ~bytes32(uint256(0xff));
    bytes32 internal constant TREASURY_STORAGE_SLOT = 0x34492fe6f157732a3925e28c9a97dd2d79c6abf4daa6ff0b4ef04f149adcfe00;

    // keccak256("GOVERNANCE_ROLE")
    bytes32 private constant GOVERNANCE_ROLE = 0x71840dc4906352362b0cdaf79870196c8e42acafade72d5d5a6d59291253ceb1;

    // keccak256("EMERGENCY_GOVERNANCE_ROLE")
    bytes32 private constant EMERGENCY_GOVERNANCE_ROLE = 0xc4982456f383374a8a4289355835629c1e1d1b4fead2a1041b76563b62f38f29;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    /// @inheritdoc ITreasuryV2
    /// @dev We cannot remove the onlyOwner modifier because we need to keep the owner()
    //       function for the upgradeability from version 1 to version 2 since during the
    ///      upgrade, the GOVERNANCE_ROLE is not set yet.
    function initializeV2(address governanceAddress, address emergencyGovernanceAddress) external onlyOwner reinitializer(2) {
        require(governanceAddress != address(0), GovernanceAddressCannotBeZeroAddress());
        require(governanceAddress != owner(), GovernanceAddressCannotBeOwner());
        require(emergencyGovernanceAddress != address(0), EmergencyGovernanceAddressCannotBeZeroAddress());
        require(emergencyGovernanceAddress != owner(), EmergencyGovernanceAddressCannotBeOwner());

        __AccessControl_init();

        _grantRole(DEFAULT_ADMIN_ROLE, governanceAddress);
        _grantRole(GOVERNANCE_ROLE, governanceAddress);
        _grantRole(EMERGENCY_GOVERNANCE_ROLE, emergencyGovernanceAddress);

        // Leaves the contract without owner. It will not be possible to call `onlyOwner` functions.
        // From now on, only the governance and emergency governance roles can call the functions
        // that previously required the owner role.
        renounceOwnership();
    }

    /// @inheritdoc ITreasuryV2
    function withdrawICNTToReserve(uint256 amount) external override whenNotPaused {
        TreasuryStorage storage $ = _getTreasuryStorageData();
        address _reserveContract = $.reserveContract;
        require(msg.sender == _reserveContract, OnlyReserveContract(_reserveContract, msg.sender));
        IERC20 _icnToken = $.icnToken;
        _icnToken.safeTransfer(_reserveContract, amount);
        emit WithdrawalToReserve(_reserveContract, _icnToken, amount);
    }

    /// @inheritdoc ITreasuryV2
    function withdraw(address tokenAddress, uint256 amount, address to)
        external
        override
        onlyRole(GOVERNANCE_ROLE)
        whenNotPaused
    {
        if (tokenAddress == NATIVE_TOKEN) {
            (bool success,) = payable(to).call{value: amount}("");
            require(success, NativeTransferFailed(to, amount));
        } else {
            IERC20(tokenAddress).safeTransfer(to, amount);
        }

        emit OwnerWithdrawal(to, tokenAddress, amount);
    }

    /// @inheritdoc ITreasuryV2
    function pause() external override onlyRole(EMERGENCY_GOVERNANCE_ROLE) {
        _pause();
    }

    /// @inheritdoc ITreasuryV2
    function unpause() external override onlyRole(EMERGENCY_GOVERNANCE_ROLE) {
        _unpause();
    }

    /// @inheritdoc ITreasuryV2
    function setICNToken(IERC20 _icnToken) external onlyRole(GOVERNANCE_ROLE) {
        require(address(_icnToken) != address(0), ICNTokenCannotBeZeroAddress());
        _getTreasuryStorageData().icnToken = _icnToken;
        emit ICNTokenSet(_icnToken);
    }

    /// @inheritdoc ITreasuryV2
    function setReserveContract(address _reserveContract) external onlyRole(GOVERNANCE_ROLE) {
        require(_reserveContract != address(0), ReserveContractCannotBeZeroAddress());
        _getTreasuryStorageData().reserveContract = _reserveContract;
        emit ReserveContractSet(_reserveContract);
    }

    /// @inheritdoc ITreasuryV2
    function icnToken() external view override returns (IERC20) {
        return _getTreasuryStorageData().icnToken;
    }

    /// @inheritdoc ITreasuryV2
    function reserveContract() external view override returns (address) {
        return _getTreasuryStorageData().reserveContract;
    }

    function _authorizeUpgrade(address) internal override onlyRole(GOVERNANCE_ROLE) {}

    function _getTreasuryStorageData() internal pure returns (TreasuryStorage storage $) {
        bytes32 slot = TREASURY_STORAGE_SLOT;
        assembly {
            $.slot := slot
        }
    }
}
