// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

interface IHPDelegationICNTErrors {
    /// @dev Error triggered when the HP Delegation ICNT rewards are already activated
    error HPDelegationRewardsAlreadyActivated();

    /// @dev Error triggered when the HP Delegation ICNT module is already initialized
    error HPDelegationICNTAlreadyInitialized();

    /// @dev Error triggered when the lockup duration is invalid
    /// @param lockupDurationInSeconds The lockup duration in seconds
    /// @param minLockupDurationInSeconds The minimum lockup duration in seconds
    /// @param maxLockupDurationInSeconds The maximum lockup duration in seconds
    error InvalidLockupDuration(
        uint256 lockupDurationInSeconds, uint256 minLockupDurationInSeconds, uint256 maxLockupDurationInSeconds
    );

    /// @dev Error triggered when the lockup duration is not allowed
    /// @param lockupDurationInSeconds The lockup duration in seconds
    error LockupDurationNotAllowed(uint256 lockupDurationInSeconds);

    /// @dev Error triggered when the delegation index is invalid
    /// @param index The delegation index
    /// @param length The length of the delegation array
    error InvalidDelegationIndex(uint256 index, uint256 length);

    /// @dev Error triggered when the unlock time is not reached
    /// @param unlockTime The unlock time
    error NotUnlocked(uint256 unlockTime);

    /// @dev Error triggered when the allow undelegate delay after staking is not met
    /// @param currentTimestamp The current timestamp
    /// @param unlockTimestamp The unlock timestamp
    error AllowUndelegateDelayAfterStakingNotMet(uint256 currentTimestamp, uint256 unlockTimestamp);

    /// @dev Error triggered when the max APY to min APY ratio is too high
    error MaxApyToMinApyRatioTooHigh();

    /// @dev Error triggered when the target collateralization rate is out of bounds
    error TargetCollateralizationRateOutOfBounds();

    /// @dev Error triggered when the max APY curve domain low should be less than high
    error MaxApyCurveDomainLowShouldBeLessThanHigh();

    /// @dev Error triggered when the collateralization rate is out of bounds
    /// @param collateralizationRate The collateralization rate
    /// @param min The minimum collateralization rate
    /// @param max The maximum collateralization rate
    error CollateralizationRateOutOfBounds(uint256 collateralizationRate, uint256 min, uint256 max);

    /// @dev Error triggered when the undelegation is already initialized
    error UndelegationAlreadyInitialized();

    /// @dev Error triggered when the unstaking is not initialized
    error UnstakingNotInitialized();

    /// @dev Error triggered when there are no unclaimed rewards
    error NoUnclaimedRewards();

    /// @dev Error triggered when the available locked tokens are insufficient
    /// @param availableLockedTokens The available locked tokens
    /// @param amount The amount
    error InsufficientUnlockedTokens(uint256 availableLockedTokens, uint256 amount);

    /// @dev Error triggered when the max APY curve should have at least one point
    error MaxApyCurveShouldHaveAtLeastOnePoint();

    /// @dev Error triggered when the min X is greater than max X
    error MinXGreaterThanMaxX();

    /// @dev Error triggered when the undelegated position cannot earn rewards
    /// @param delegator The delegator
    /// @param delegationIndex The delegation index
    /// @param nodeDelegationIndex The node delegation index
    error UndelegatedPositionCannotEarnRewards(address delegator, uint256 delegationIndex, uint256 nodeDelegationIndex);

    /// @dev Error triggered when the pending rewards claim index is invalid
    /// @param pendingRewardsClaimIndex The pending rewards claim index
    /// @param length The length of the pending rewards claims array
    error InvalidPendingRewardsClaimIndex(uint256 pendingRewardsClaimIndex, uint256 length);

    /// @dev Error triggered when the amount is invalid
    /// @param amount The amount
    /// @param minAmount The minimum amount
    error InvalidAmount(uint256 amount, uint256 minAmount);

    /// @dev Error triggered when the locked and node delegation indexes lengths mismatch
    /// @param lockedDelegationIndexesLength The length of the locked delegation indexes
    /// @param nodeDelegationIndexesLength The length of the node delegation indexes
    error LockedAndNodeDelegationIndexesLengthMismatch(uint256 lockedDelegationIndexesLength, uint256 nodeDelegationIndexesLength);

    /// @dev Error triggered when the locked delegation index is invalid
    /// @param lockedDelegationIndex The locked delegation index
    /// @param length The length of the locked delegations array
    error InvalidLockedDelegationIndex(uint256 lockedDelegationIndex, uint256 length);

    /// @dev Error triggered when the node delegation index is invalid
    /// @param nodeDelegationIndex The node delegation index
    /// @param length The length of the node delegations array
    error InvalidNodeDelegationIndex(uint256 nodeDelegationIndex, uint256 length);

    /// @dev Error triggered when the lengths are invalid
    /// @param length1 The length 1
    /// @param length2 The length 2
    error InvalidLengths(uint256 length1, uint256 length2);

    /// @dev Error triggered when the scaler node must be verified for delegation
    /// @param nodeId The node ID
    error ScalerNodeMustBeVerifiedForDelegation(uint256 nodeId);

    /// @dev Error triggered when the allow reclaim delay after initiation is not met
    /// @param currentEra The current era
    /// @param reclaimAllowedAfterEra The reclaim allowed after era
    error AllowReclaimDelayAfterInitiationNotMet(uint256 currentEra, uint256 reclaimAllowedAfterEra);
}
