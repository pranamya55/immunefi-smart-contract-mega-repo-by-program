// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

import {IAccessControlStorage} from "./interfaces/IAccessControlStorage.sol";

contract AccessControlStorage is IAccessControlStorage {
    /// @custom:storage-location erc7201:accesscontrol.storage
    struct AccessControlStorageData {
        uint64 version;
        /// @dev DEPRECATED in v5.1.0: use `_roles` instead, `roles` is used to store the roles before v5.1.0 of the access control
        mapping(address => bytes32) roles;
        bool paused;
        /// @dev `_roles` is used to store the roles starting v5.1.0 of the access control
        mapping(bytes32 role => mapping(address account => bool hasRole)) _roles;
    }

    // keccak256("DEFAULT_ADMIN_ROLE")
    /// @dev DEPRECATED in v5.1.0: use `GOVERNANCE_ROLE` instead, should not be used anymore
    bytes32 internal constant DEFAULT_ADMIN_ROLE = 0x1effbbff9c66c5e59634f24fe842750c60d18891155c32dd155fc2d661a4c86d;

    // keccak256("ICN_OPERATOR_ROLE")
    bytes32 internal constant ICN_OPERATOR_ROLE = 0x76bca8e47b2c8cfd6ce42bb904374bbf3437835b1a7a236ec311101a21a60567;

    // keccak256("GOVERNANCE_ROLE")
    bytes32 internal constant GOVERNANCE_ROLE = 0x71840dc4906352362b0cdaf79870196c8e42acafade72d5d5a6d59291253ceb1;

    // keccak256("EMERGENCY_GOVERNANCE_ROLE")
    bytes32 internal constant EMERGENCY_GOVERNANCE_ROLE = 0xc4982456f383374a8a4289355835629c1e1d1b4fead2a1041b76563b62f38f29;

    // keccak256("PRODUCT_ROLE")
    bytes32 internal constant PRODUCT_ROLE = 0xb07f4d07255abd04ebad1608ac8dbe90c6bcd81ab6206be2c175324838dba6f3;

    // keccak256("TOKENOMICS_ROLE")
    bytes32 internal constant TOKENOMICS_ROLE = 0xe9ee4c33e7347984e3a65fa7bb2d27f7fbe954d1f42b8b3a9d7d0d919f5c39a9;

    // keccak256(abi.encode(uint256(keccak256("accesscontrol.storage")) - 1)) & ~bytes32(uint256(0xff));
    bytes32 internal constant ACCESS_CONTROL_STORAGE_SLOT = 0xce204c5909703ef7c50378b96db285374dfb2bd7ec9469114207e28a4e4de000;

    /// @dev Modifier that checks that an account has a specific role. Reverts with an
    /// {AccessControlUnauthorizedAccount} error including the required role.
    modifier onlyRole(bytes32 role) {
        require(_hasRole(role, msg.sender), AccessControlUnauthorizedAccount(msg.sender, role));
        _;
    }

    /// @dev Modifier that checks that the caller is the self. Reverts with an
    /// {AccessControlUnauthorizedSelf} error including the caller.
    modifier onlySelf() {
        require(msg.sender == address(this), AccessControlUnauthorizedSelf(msg.sender, address(this)));
        _;
    }

    /// @dev Modifier to check if the contract is not paused
    modifier whenNotPaused() {
        require(!getAccessControlStorage().paused, AccessControlPaused());
        _;
    }

    /// @dev Modifier to check if the contract is paused
    modifier whenPaused() {
        require(getAccessControlStorage().paused, AccessControlNotPaused());
        _;
    }

    function _hasRole(bytes32 role, address account) internal view returns (bool) {
        AccessControlStorageData storage $ = getAccessControlStorage();
        return $.roles[account] == role || $._roles[role][account];
    }

    function getAccessControlStorage() internal pure returns (AccessControlStorageData storage $) {
        bytes32 slot = ACCESS_CONTROL_STORAGE_SLOT;
        assembly {
            $.slot := slot
        }
    }
}
