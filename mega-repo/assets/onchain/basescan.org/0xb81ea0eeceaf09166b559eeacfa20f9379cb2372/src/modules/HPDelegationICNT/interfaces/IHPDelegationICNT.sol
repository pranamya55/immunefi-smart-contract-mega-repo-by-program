// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

import {IHPDelegationICNTErrors} from "./IHPDelegationICNTErrors.sol";
import {IHPDelegationICNTStorage} from "./IHPDelegationICNTStorage.sol";

interface IHPDelegationICNT is IHPDelegationICNTErrors, IHPDelegationICNTStorage {
    /// @notice Emitted when the module has been initialized.
    event HPDelegationModuleInitialized();

    /// @notice Emitted when the module has been initialized.
    event HPDelegationICNTModuleInitializedV2();

    /// @notice Emitted when the module has been initialized.
    event HPDelegationICNTModuleInitializedV3();

    /// @notice Emitted when collateral is delegated.
    /// @param nodeId The ID of the node
    /// @param delegator The address of the delegator
    /// @param amount The amount of collateral delegated
    /// @param apyScalingFactor The APY scaling factor for the delegation
    /// @param unlockTimestamp The timestamp when the collateral can be unlocked
    event CollateralDelegated(
        uint256 indexed nodeId,
        address indexed delegator,
        uint256 indexed amount,
        uint256 apyScalingFactor,
        uint256 unlockTimestamp
    );

    /// @notice Emitted when collateral is delegated.
    /// @param nodeId The ID of the node
    /// @param lockedDelegationIndex The index of the locked delegation
    /// @param delegator The address of the delegator
    /// @param apyScalingFactor The APY scaling factor for the delegation
    /// @param unlockTimestamp The timestamp when the collateral can be unlocked
    /// @param amount The amount of collateral delegated
    event CollateralDelegatedV2(
        uint256 indexed nodeId,
        uint256 indexed lockedDelegationIndex,
        address indexed delegator,
        uint256 apyScalingFactor,
        uint256 unlockTimestamp,
        uint256 amount
    );

    /// @notice Emitted when a delegation is created.
    /// @param nodeId The ID of the node
    /// @param delegator The address of the delegator
    /// @param lockedDelegationIndex The index of the locked delegation
    /// @param apyScalingFactor The APY scaling factor for the delegation
    /// @param unlockTimestamp The timestamp when the collateral can be unlocked
    /// @param amount The amount of collateral delegated
    event DelegationCreated(
        uint256 indexed nodeId,
        address indexed delegator,
        uint256 indexed lockedDelegationIndex,
        uint256 apyScalingFactor,
        uint256 unlockTimestamp,
        uint256 amount
    );

    /// @notice Emitted when a pending rewards are claimed.
    /// @param delegator The address of the delegator
    /// @param lockedDelegationIndex The array of indexes of the locked delegation
    /// @param nodeDelegationIndex The array of indexes of the node delegation
    /// @param claimIndex The index of the claim created
    /// @param amounts The amount of pending rewards
    /// @param unlockTimestamp The timestamp when the pending rewards can be claimed
    event PendingRewardsClaimed(
        address indexed delegator,
        uint256[] lockedDelegationIndex,
        uint256[] nodeDelegationIndex,
        uint256 claimIndex,
        uint256[] amounts,
        uint256 unlockTimestamp
    );

    /// @notice Emitted when network collateral is withdrawn.
    /// @param delegator The address of the delegator
    /// @param amount The amount of collateral withdrawn
    /// @param rewards The amount of rewards withdrawn
    /// @param lockupDurationInSeconds The lockup duration in seconds
    /// @param nodeId The ID of the node
    event NetworkCollateralWithdrawn(
        address indexed delegator, uint256 indexed amount, uint256 indexed rewards, uint256 lockupDurationInSeconds, string nodeId
    );

    /// @notice Emitted when the target collateralization rate is set.
    /// @param targetCollateralizationRate The target collateralization rate
    event TargetCollateralizationRateSet(uint256 indexed targetCollateralizationRate);

    /// @notice Emitted when the max APY to min APY ratio is set.
    /// @param maxApyToMinApyRatio The max APY to min APY ratio
    event MaxApyToMinApyRatioSet(uint256 indexed maxApyToMinApyRatio);

    /// @notice Emitted when the max APY curve is set.
    /// @param maxApyCurve The max APY curve
    event MaxApyCurveSet(uint256[] maxApyCurve);

    /// @notice Emitted when the delegator rewards are committed.
    /// @param maxApy The max APY
    /// @param secondsSinceCommit The seconds since the last commit
    /// @param baseIncentiveAccumulation The base incentive accumulation
    event DelegatorRewardsCommitted(
        uint256 indexed maxApy, uint256 indexed secondsSinceCommit, uint256 indexed baseIncentiveAccumulation
    );

    /// @notice Emitted when the allow unstake delay after staking is set.
    /// @param allowUnstakeDelayAfterStakingInSeconds The allow unstake delay after staking in seconds
    event AllowUnstakeDelayAfterStakingInSecondsSet(uint256 indexed allowUnstakeDelayAfterStakingInSeconds);

    /// @notice Emitted when the allow unstake delay after initiation is set.
    /// @param allowReclaimDelayAfterUnstakeInEras The allow unstake delay after initiation in seconds
    event AllowReclaimDelayAfterUnstakeInErasSet(uint256 indexed allowReclaimDelayAfterUnstakeInEras);

    /// @notice Emitted when the allow reward claim delay after staking is set.
    /// @param allowRewardClaimDelayAfterStakingInSeconds The allow reward claim delay after staking in seconds
    event AllowRewardClaimDelayAfterStakingInSecondsSet(uint256 indexed allowRewardClaimDelayAfterStakingInSeconds);

    /// @notice Emitted when collateral is reclaimed.
    /// @param delegator The address of the delegator
    /// @param lockedDelegationIndex The index of the locked delegation
    /// @param nodeDelegationIndex The index of the node delegation
    event CollateralReclaimed(
        address indexed delegator, uint256 indexed lockedDelegationIndex, uint256 indexed nodeDelegationIndex
    );

    /// @notice Emitted when collateral is undelegated.
    /// @param delegator The address of the delegator
    /// @param lockedDelegationIndex The index of the locked delegation
    /// @param nodeDelegationIndex The index of the node delegation
    event CollateralUndelegated(
        address indexed delegator, uint256 indexed lockedDelegationIndex, uint256 indexed nodeDelegationIndex
    );

    /// @notice Emitted when rewards are delegated.
    /// @param delegator The address of the delegator
    /// @param nodeId The ID of the node
    /// @param amount The amount of rewards delegated
    /// @param lockupDurationInSeconds The lockup duration in seconds
    event RewardsDelegated(
        address indexed delegator, uint256 indexed nodeId, uint256 indexed amount, uint256 lockupDurationInSeconds
    );

    /// @notice Emitted when pending rewards claim is initialized.
    /// @param delegator The address of the delegator
    /// @param amount The amount of pending rewards
    /// @param unlockTimestamp The timestamp when the pending rewards can be claimed
    event PendingRewardsClaimInitialized(address indexed delegator, uint256 indexed amount, uint256 unlockTimestamp);

    /// @notice Emitted when HP Delegation ICNT rewards are claimed.
    /// @param delegator The address of the delegator
    /// @param amount The amount of rewards claimed
    event HPDelegationICNTRewardsClaimed(address indexed delegator, uint256 indexed amount);

    /// @notice Emitted when HP Delegation ICNT rewards are claimed with the pending rewards claim index
    /// @param delegator The address of the delegator
    /// @param pendingRewardsClaimIndex The index of the pending rewards claim
    /// @param amount The amount of rewards claimed
    event HPDelegationICNTRewardsClaimedV2(address indexed delegator, uint256 indexed pendingRewardsClaimIndex, uint256 amount);

    /// @notice Emitted when unlocked tokens are withdrawn.
    /// @param delegator The address of the delegator
    /// @param lockedDelegationIndex The index of the locked delegation
    /// @param amount The amount of tokens withdrawn
    event UnlockedTokensWithdrawn(address indexed delegator, uint256 indexed lockedDelegationIndex, uint256 indexed amount);

    /// @notice Emitted when the HP delegation rewards are activated.
    event HPDelegationRewardsActivated();

    /// @notice Emitted when the scaling factors are set.
    /// @param scalingFactorC1 The scaling factor C1
    /// @param scalingFactorC2 The scaling factor C2
    /// @param scalingFactorC3 The scaling factor C3
    event ScalingFactorsSet(uint256 indexed scalingFactorC1, uint256 indexed scalingFactorC2, uint256 indexed scalingFactorC3);

    /// @notice Initializes the HP Staking ICNT contract
    /// @param _maxApyCurve The max APY curve
    /// @param _allowUnstakeDelayAfterStakingInSeconds The delay in seconds after staking before unstaking is allowed
    /// @param _allowReclaimDelayAfterUnstakeInEras The delay in eras after unstaking before restaking is allowed
    /// @param _allowRewardClaimDelayAfterStakingInSeconds The delay in seconds after staking before reward claims are allowed
    function initializeHPDelegationICNT(
        uint256[] calldata _maxApyCurve,
        uint256 _allowUnstakeDelayAfterStakingInSeconds,
        uint256 _allowReclaimDelayAfterUnstakeInEras,
        uint256 _allowRewardClaimDelayAfterStakingInSeconds
    ) external;

    /// @notice Delegates network collateral to the HP's vault
    /// @param _nodeId The ID of the node
    /// @param _amount The amount of network collateral to delegate
    /// @param _lockupDurationInSeconds The lockup duration in seconds
    function delegateCollateral(uint256 _nodeId, uint256 _amount, uint256 _lockupDurationInSeconds) external;

    /// @notice Delegates already locked ICNT to the HP's vault
    /// @param _nodeId The ID of the node
    /// @param _amount The amount of network collateral to delegate
    /// @param _lockedDelegationIndex The index of the locked delegation
    function delegateLockedCollateral(uint256 _nodeId, uint256 _amount, uint256 _lockedDelegationIndex) external;

    /// @notice Delegates collateral from node rewards to the HP's vault
    /// @param _nodeId The ID of the node
    /// @param _amount The amount of collateral to delegate
    /// @param _delegator The address of the delegator
    /// @param _lockupDurationInSeconds The lockup duration in seconds
    function delegateCollateralFromNodeRewards(
        uint256 _nodeId,
        uint256 _amount,
        address _delegator,
        uint256 _lockupDurationInSeconds
    ) external;

    /// @notice Delegates collateral from link rewards to the HP's vault
    /// @param _nodeId The ID of the node
    /// @param _amount The amount of collateral to delegate
    /// @param _delegator The address of the delegator
    /// @param _lockupDurationInSeconds The lockup duration in seconds
    function delegateCollateralFromLinkRewards(
        uint256 _nodeId,
        uint256 _amount,
        address _delegator,
        uint256 _lockupDurationInSeconds
    ) external;

    /// @notice Initiates the undelegation process for a locked delegation
    /// @notice After a delay, the user can reclaim the undelegated collateral
    /// @notice The delegators stops receiving rewards after the undelegation is initiated
    /// @param _lockedDelegationIndex The index of the locked delegation
    /// @param _nodeDelegationIndex The index of the node delegation
    function undelegateCollateral(uint256 _lockedDelegationIndex, uint256 _nodeDelegationIndex) external;

    /// @notice Deletes the Locked Delegation Entry and Makes the tokens available for withdrawal or re-delegation to another node
    /// @param _lockedDelegationIndex The index of the locked delegation
    /// @param _nodeDelegationIndex The index of the node delegation
    function reclaimUndelegatedCollateral(uint256 _lockedDelegationIndex, uint256 _nodeDelegationIndex) external;

    /// @notice Withdraws unlocked tokens
    /// @param _lockedDelegationIndex The index of the locked delegation
    /// @param _amount The amount of tokens to withdraw
    function withdrawUnlockedDelegatedTokens(uint256 _lockedDelegationIndex, uint256 _amount) external;

    /// @notice Delegates unclaimed rewards to the HP's vault immediately, without a delay
    /// @param _lockedDelegationIndex The index of the locked delegation
    /// @param _nodeDelegationIndex The index of the node delegation
    /// @param _nodeId The ID of the node
    /// @param _lockupDurationInSeconds The lockup duration in seconds
    function delegateUnclaimedRewards(
        uint256 _lockedDelegationIndex,
        uint256 _nodeDelegationIndex,
        uint256 _nodeId,
        uint256 _lockupDurationInSeconds
    ) external;

    /// @notice Initializes the claim process for pending rewards
    /// @param _lockedDelegationIndex The index of the locked delegation
    /// @param _nodeDelegationIndex The index of the node delegation
    function initiateDelegationRewardsClaim(uint256 _lockedDelegationIndex, uint256 _nodeDelegationIndex) external;

    /// @notice Initializes the claim process for pending rewards
    /// @param _lockedDelegationIndexes The array of indexes of locked delegations
    /// @param _nodeDelegationIndexes The array of indexes of node delegations
    function batchInitiateDelegationRewardsClaim(
        uint256[] calldata _lockedDelegationIndexes,
        uint256[] calldata _nodeDelegationIndexes
    ) external;

    /// @notice Claims pending rewards
    /// @param _pendingRewardsClaimIndex The index of the pending rewards claim
    function claimDelegationRewards(uint256 _pendingRewardsClaimIndex) external;

    /// @notice Sets the max APY curve values
    /// @param _maxApyCurve The max APY curve
    function setMaxApyCurve(uint256[] calldata _maxApyCurve) external;

    /// @notice Sets the allow unstake delay after staking in seconds
    /// @param _allowUnstakeDelayAfterStakingInSeconds The delay in seconds after staking before unstaking is allowed
    function setAllowUnstakeDelayAfterStakingInSeconds(uint256 _allowUnstakeDelayAfterStakingInSeconds) external;

    /// @notice Sets the allow unstake delay after initiation in seconds
    /// @param _allowReclaimDelayAfterUnstakeInEras The delay in seconds after unstaking before restaking is allowed
    function setAllowReclaimDelayAfterUnstakeInEras(uint256 _allowReclaimDelayAfterUnstakeInEras) external;

    /// @notice Sets the allow reward claim delay after staking in seconds
    /// @param _allowRewardClaimDelayAfterStakingInSeconds The delay in seconds after staking before reward claims are allowed
    function setAllowRewardClaimDelayAfterStakingInSeconds(uint256 _allowRewardClaimDelayAfterStakingInSeconds) external;

    /// @notice Sets the scaling factors
    /// @param _scalingFactorC1 The scaling factor C1
    /// @param _scalingFactorC2 The scaling factor C2
    /// @param _scalingFactorC3 The scaling factor C3
    function setScalingFactors(uint256 _scalingFactorC1, uint256 _scalingFactorC2, uint256 _scalingFactorC3) external;

    /// @notice Activates the HP delegation rewards.
    function activateDelegationRewards() external;

    /// @notice Returns the unclaimed rewards for a delegator
    /// @param delegator The address of the delegator
    /// @param delegationIndex The index of the delegation
    /// @param nodeDelegationIndex The index of the node delegation
    /// @return The unclaimed rewards
    function unclaimedDelegationRewards(address delegator, uint256 delegationIndex, uint256 nodeDelegationIndex)
        external
        view
        returns (uint256);

    /// @notice Returns the total amount of ICNT delegated to the HP's vault
    /// @return The total amount of ICNT delegated to the HP's vault
    function getTotalDelegatedICNT() external view returns (uint256);

    /// @notice Returns the total amount of ICNT delegated to a node
    /// @param nodeId The ID of the node
    /// @return The total amount of ICNT delegated to the node
    function getNodeTotalDelegatedICNT(uint256 nodeId) external view returns (uint256);

    /// @notice Returns the delegation for a delegator
    /// @param delegator The address of the delegator
    /// @param index The index of the delegation
    /// @return The delegation
    function getDelegation(address delegator, uint256 index) external view returns (UserDelegation memory);

    /// @notice Returns the delegations for a delegator
    /// @param delegator The address of the delegator
    /// @return The delegations
    function getDelegations(address delegator) external view returns (UserDelegation[] memory);

    /// @notice Returns the pending rewards claims for a delegator
    /// @param delegator The address of the delegator
    /// @return The pending rewards claims
    function getPendingDelegatorRewardsClaims(address delegator) external view returns (PendingUserRewardClaims[] memory);

    /// @notice Returns the allow initiate unstake delay after staking in seconds
    /// @return The allow initiate unstake delay after staking in seconds
    function getAllowUnstakeDelayAfterStakingInSeconds() external view returns (uint256);

    /// @notice Returns the allow unstake delay after initiation in seconds
    /// @return The allow unstake delay after initiation in seconds
    function getAllowReclaimDelayAfterUnstakeInEras() external view returns (uint256);

    /// @notice Returns the allow reward claim delay after staking in seconds
    /// @return The allow reward claim delay after staking in seconds
    function getAllowRewardClaimDelayAfterStakingInSeconds() external view returns (uint256);

    /// @notice Returns the max APY curve values
    /// @return The max APY curve values
    function getMaxApyCurve() external view returns (uint256[] memory);

    /// @notice Returns the last reward commitment timestamp
    /// @return The last reward commitment timestamp
    function getLastRewardCommitmentTimestamp() external view returns (uint256);

    /// @notice Returns the scaling factors
    /// @return The scaling factors
    function getScalingFactors() external view returns (uint256, uint256, uint256);

    /// @notice Calculates the max APY for a given collateralization rate
    /// @param _collateralizationRate The collateralization rate
    /// @return The max APY
    function calculateMaxApy(uint256 _collateralizationRate) external view returns (uint256);

    /// @notice Calculates the scaled APY for a given collateralization rate and locking duration
    /// @param _collateralizationRate The collateralization rate
    /// @param _lockingDurationInSeconds The locking duration in seconds
    /// @return The scaled APY
    function calculateScaledApy(uint256 _collateralizationRate, uint256 _lockingDurationInSeconds)
        external
        view
        returns (uint256);

    /// @notice Returns the version of the HP Delegation ICNT module
    /// @return The version of the HP Delegation ICNT module
    function getHPDelegationICNTVersion() external view returns (uint64);
}
