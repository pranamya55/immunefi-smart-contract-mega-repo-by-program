// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

/// @title ITreasuryErrorsV2
/// @dev Interface for custom errors for the TreasuryV2 contract.
interface ITreasuryErrorsV2 {
    /// @dev Error triggered when the only reserve contract is required
    /// @param expected The expected address of the reserve contract
    /// @param actual The actual address of the reserve contract
    error OnlyReserveContract(address expected, address actual);

    /// @dev Error triggered when the native transfer fails
    /// @param to The address of the recipient
    /// @param amount The amount of tokens to transfer
    error NativeTransferFailed(address to, uint256 amount);

    /// @dev Error triggered when the ICNT token cannot be zero address
    error ICNTokenCannotBeZeroAddress();

    /// @dev Error triggered when the reserve contract cannot be zero address
    error ReserveContractCannotBeZeroAddress();

    /// @dev Error triggered when the governance address cannot be zero address
    error GovernanceAddressCannotBeZeroAddress();

    /// @dev Error triggered when the governance address cannot be the owner
    error GovernanceAddressCannotBeOwner();

    /// @dev Error triggered when the emergency governance address cannot be zero address
    error EmergencyGovernanceAddressCannotBeZeroAddress();

    /// @dev Error triggered when the emergency governance address cannot be the owner
    error EmergencyGovernanceAddressCannotBeOwner();
}
