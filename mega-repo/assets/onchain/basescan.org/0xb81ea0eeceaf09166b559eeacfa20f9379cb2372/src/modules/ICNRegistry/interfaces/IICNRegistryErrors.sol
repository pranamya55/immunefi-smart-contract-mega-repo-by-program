// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

/// @dev Interface for custom errors for the ICNRegistry operations.

interface IICNRegistryErrors {
    /// @dev Error triggered when the contract has already been initialized
    error ICNRegistryAlreadyInitialized();

    /// @dev Error triggered when an invalid parameter is passed
    error ICNRegistryInvalidParams();

    /// @dev Error triggered when a node has invalid name length
    error InvalidName(uint256 actual, uint256 min, uint256 max);

    /// @dev Error triggered when there is an attempt to register a region / cluster / node with invalid regionId
    error InvalidRegion();

    /// @dev Error triggered when there is an attempt to register a region with invalid target capacity
    error InvalidTargetCapacity();

    /// @dev Error triggered when there is an attempt to register a region with invalid collateral amount
    error InvalidCollateralReq();

    /// @dev Error triggered when there is an attempt to register a region with invalid release schedule end timestamp
    error InvalidReleaseScheduleEndTimestamp();

    /// @dev Error triggered when there is an attempt to register a cluster with invalid clusterId
    error InvalidCluster();

    /// @dev Error triggered when there is an attempt to register a HP with invalid account
    error InvalidHP();

    /// @dev Error triggered when there is an attempt to register a SP with invalid account
    error InvalidSP();

    /// @dev Error triggered when there is an attempt to register a Scaler Node with invalid scalerNodeId
    error InvalidScalerNode();

    /// @dev Error triggered when there is an attempt to update a HyperNode with invalid hyperNodeId
    error InvalidHyperNode();

    /// @dev Error triggered when there is an attempt to register a Node with invalid commitment duration
    error InvalidCommitmentDuration();

    /// @dev Error triggered when there is an attempt to register a Node in a cluster that has reached its max node registration.
    error TooManyNodes();

    /// @dev Error triggered when there is an attempt to remove a Node with invalid caller
    error InvalidCaller();

    /// @dev Error triggered when there is a missmatch between the hardware class in the cluster and the node being registered
    error HardwareClassMismatch();

    /// @dev Error triggered when there is an attempt to register a Node with invalid collateral amount provided
    error NotEnoughCollateral();

    /// @dev Error triggered when there is an attempt to call a function with an unauthorized account
    /// @param actualCaller The actual caller
    /// @param expectedCaller The expected caller
    error ICNRegistryUnauthorizedAccount(address actualCaller, address expectedCaller);

    /// @dev Error triggered when there is an attempt to register a hardware class that has already been registered
    error HwClassAlreadyRegistered();

    /// @dev Error triggered when there is an attempt to register a hardware class that has already been registered
    error InvalidHwClass();

    /// @dev Error triggered when there is an attempt to register a hardware class with invalid capacity
    error InvalidCapacity();

    /// @dev Error triggered when there is an attempt to register a hardware class with invalid reason
    error InvalidReason();

    /// @dev Error triggered when there is an attempt to register a hardware class with invalid minimum collateral percent
    error InvalidMinCollateralPercent(uint256 actual, uint256 min, uint256 max);

    /// @dev Error triggered when there is an attempt to setup invalid market adjustment factor
    error InvalidMarketAdjustmentFactor();

    /// @dev Error triggered when there is an attempt to set a protocol margin that is higher than 100%
    error InvalidProtocolMargin();

    /// @dev Error triggered when there is an attempt to verify scaler node with invalid daemon address
    error InvalidDaemonAddress();

    /// @dev Error triggered when the public key is duplicated
    error DuplicatePublicKey(address publicKey);

    /// @dev Error triggered when there is an attempt to increase node collateral with invalid collateral amount
    error InvalidCollateralAmount();

    /// @dev Error triggered when there is an attempt to update a scaler node reservation price with invalid reservation price
    error InvalidReservationPrice();

    /// @dev Error triggered when there is an attempt to update a scaler node node reward share with invalid node reward share
    error InvalidNodeRewardShare();

    /// @dev Error triggered when input array length mismatch
    error ICNRegistryInvalidLength();

    /// @dev Error triggered when there is an attempt to update a SN reservation price with too long batch array length
    error TooManyScalerNodes();

    /// @dev Error triggered when there is an attempt register a booking on a node that is already booked
    error UtilizedCapacityNotNull();
}
