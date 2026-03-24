// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

/// @title IAccessControlStorageErrors
/// @dev Interface for custom errors for the AccesControlStorage operations.
interface IAccessControlStorageErrors {
    /// @dev The `account` is missing a role.
    error AccessControlUnauthorizedAccount(address account, bytes32 neededRole);

    /// @dev The `account` is not the self.
    error AccessControlUnauthorizedSelf(address account, address self);

    /// @dev Error triggered when the contract is paused
    error AccessControlPaused();

    /// @dev Error triggered when the contract is not paused
    error AccessControlNotPaused();
}
