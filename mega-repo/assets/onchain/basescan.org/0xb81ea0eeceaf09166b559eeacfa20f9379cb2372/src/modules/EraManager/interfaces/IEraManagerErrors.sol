// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

/// @title IEraManagerErrors
/// @dev Interface for custom errors for the EraManager operations.
interface IEraManagerErrors {
    /// @dev Error triggered when a function is called with arguments that are not valid
    ///      under the expected operational conditions.
    error EraManagerInvalidArguments();

    /// @dev Error triggered when no era segments are available
    error NoEraSegments();

    /// @dev Error triggered when an era has not started
    error EraNotStarted();

    /// @dev Error triggered when the EraManager is already initialized
    error EraManagerAlreadyInitialized();
}
