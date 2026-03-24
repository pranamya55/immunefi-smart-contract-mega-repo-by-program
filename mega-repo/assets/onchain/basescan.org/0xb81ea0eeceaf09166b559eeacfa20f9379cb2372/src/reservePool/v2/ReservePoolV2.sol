// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {AccessControlUpgradeable} from "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";
import {Ownable2StepUpgradeable} from "@openzeppelin/contracts-upgradeable/access/Ownable2StepUpgradeable.sol";
import {PausableUpgradeable} from "@openzeppelin/contracts-upgradeable/utils/PausableUpgradeable.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {Initializable} from "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import {UUPSUpgradeable} from "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";

import {IReservePoolV2} from "./interfaces/IReservePoolV2.sol";

/// @custom:oz-upgrades-from ReservePool
contract ReservePoolV2 is
    Initializable,
    UUPSUpgradeable,
    IReservePoolV2,
    Ownable2StepUpgradeable,
    PausableUpgradeable,
    AccessControlUpgradeable
{
    using SafeERC20 for IERC20;

    /// @custom:storage-location erc7201:reservePool.storage
    struct ReservePoolStorage {
        IERC20 icnToken;
        address protocolContract;
        mapping(string => BaseReward) regionReward;
        uint256 depositedAmount;
        mapping(address => bool) isWhitelisted;
    }

    struct BaseReward {
        uint256 baseReward;
        uint256 withdrawnReward;
    }

    // keccak256(abi.encode(uint256(keccak256("reservePool.storage")) - 1)) & ~bytes32(uint256(0xff));
    bytes32 internal constant RESERVE_POOL_STORAGE_SLOT = 0x1061a7c44aaab3c559071796bd1d509825fd1f34cf6920078994646b40f9fe00;

    // keccak256("GOVERNANCE_ROLE")
    bytes32 private constant GOVERNANCE_ROLE = 0x71840dc4906352362b0cdaf79870196c8e42acafade72d5d5a6d59291253ceb1;

    // keccak256("EMERGENCY_GOVERNANCE_ROLE")
    bytes32 private constant EMERGENCY_GOVERNANCE_ROLE = 0xc4982456f383374a8a4289355835629c1e1d1b4fead2a1041b76563b62f38f29;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    /// @inheritdoc IReservePoolV2
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

    /// @inheritdoc IReservePoolV2
    function deposit(uint256 depositAmount) external override {
        require(depositAmount != 0, InvalidDepositAmount());
        ReservePoolStorage storage $ = _getReservePoolStorageData();
        require($.isWhitelisted[msg.sender], SenderNotWhitelisted());

        $.icnToken.safeTransferFrom(msg.sender, address(this), depositAmount);

        $.depositedAmount += depositAmount;

        emit DepositedAmountFromWhitelistedAccount(msg.sender, depositAmount);
    }

    /// @inheritdoc IReservePoolV2
    function withdraw(address to, uint256 amount) external override whenNotPaused {
        ReservePoolStorage storage $ = _getReservePoolStorageData();
        address _protocolContract = $.protocolContract;
        require(_protocolContract != address(0), ProtocolContractNotSet());
        require(msg.sender == _protocolContract, OnlyProtocolContract(_protocolContract, msg.sender));
        require(amount <= $.depositedAmount, AmountExceedDeposited());

        unchecked {
            $.depositedAmount -= amount;
        }

        IERC20 _icnToken = $.icnToken;
        _icnToken.safeTransfer(to, amount);

        emit OwnerWithdrawal(to, amount);
    }

    /// @inheritdoc IReservePoolV2
    function pause() external override onlyRole(EMERGENCY_GOVERNANCE_ROLE) {
        _pause();
    }

    /// @inheritdoc IReservePoolV2
    function unpause() external override onlyRole(EMERGENCY_GOVERNANCE_ROLE) {
        _unpause();
    }

    /// @inheritdoc IReservePoolV2
    function setProtocolContract(address _protocolContract) external override onlyRole(GOVERNANCE_ROLE) {
        require(_protocolContract != address(0), ProtocolContractCannotBeZeroAddress());
        _getReservePoolStorageData().protocolContract = _protocolContract;
        emit ProtocolContractSet(_protocolContract);
    }

    /// @inheritdoc IReservePoolV2
    function setICNToken(IERC20 _icnToken) external override onlyRole(GOVERNANCE_ROLE) {
        require(address(_icnToken) != address(0), ICNTokenCannotBeZeroAddress());
        _getReservePoolStorageData().icnToken = _icnToken;
        emit ICNTokenSet(_icnToken);
    }

    /// @inheritdoc IReservePoolV2
    function whitelistAccount(address account) external override onlyRole(GOVERNANCE_ROLE) {
        require(account != address(0), AccountCannotBeZeroAddress());
        ReservePoolStorage storage $ = _getReservePoolStorageData();
        require(!$.isWhitelisted[account], AccountAlreadyWhitelisted());

        $.isWhitelisted[account] = true;

        emit AccountWhitelisted(account);
    }

    /// @inheritdoc IReservePoolV2
    function unWhitelistAccount(address account) external override onlyRole(GOVERNANCE_ROLE) {
        require(account != address(0), AccountCannotBeZeroAddress());
        ReservePoolStorage storage $ = _getReservePoolStorageData();
        require($.isWhitelisted[account], AccountNotWhitelisted());

        $.isWhitelisted[account] = false;

        emit AccountUnwhitelisted(account);
    }

    /// @inheritdoc IReservePoolV2
    function icnToken() external view override returns (IERC20) {
        return _getReservePoolStorageData().icnToken;
    }

    function _authorizeUpgrade(address) internal override onlyRole(GOVERNANCE_ROLE) {}

    function _getReservePoolStorageData() internal pure returns (ReservePoolStorage storage $) {
        bytes32 slot = RESERVE_POOL_STORAGE_SLOT;
        assembly {
            $.slot := slot
        }
    }
}
