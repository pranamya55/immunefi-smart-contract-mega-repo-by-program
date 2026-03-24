// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

/// @title IReservePoolErrorsV2
/// @dev Interface for custom errors for the ReservePoolV2 contract.
interface IReservePoolErrorsV2 {
    /// @dev Error triggered when the only protocol contract is required
    /// @param expected The expected address of the protocol contract
    /// @param actual The actual address of the protocol contract
    error OnlyProtocolContract(address expected, address actual);

    /// @dev Error triggered when the ICN token cannot be zero address
    error ICNTokenCannotBeZeroAddress();

    /// @dev Error triggered when the protocol contract cannot be zero address
    error ProtocolContractCannotBeZeroAddress();

    /// @dev Error triggered when trying to whitelist zero address
    error AccountCannotBeZeroAddress();

    /// @dev Error triggered when trying to whitelist account already whitelisted
    error AccountAlreadyWhitelisted();

    /// @dev Error triggered when trying to unwhitelist not whitelisted account
    error AccountNotWhitelisted();

    /// @dev Error triggered when trying to deposit 0 tokens
    error InvalidDepositAmount();

    /// @dev Error triggered when non whitelisted account tries to deposit
    error SenderNotWhitelisted();

    /// @dev Error triggered when the protocol contract is not set
    error ProtocolContractNotSet();

    /// @dev error triggered when baseReward for given region is exceeded
    error AmountExceedBaseReward();

    /// @dev error triggered when reward exceeds deposited amount
    error AmountExceedDeposited();

    /// @dev Error triggered when the governance address cannot be zero address
    error GovernanceAddressCannotBeZeroAddress();

    /// @dev Error triggered when the governance address cannot be the owner
    error GovernanceAddressCannotBeOwner();

    /// @dev Error triggered when the emergency governance address cannot be zero address
    error EmergencyGovernanceAddressCannotBeZeroAddress();

    /// @dev Error triggered when the emergency governance address cannot be the owner
    error EmergencyGovernanceAddressCannotBeOwner();
}
