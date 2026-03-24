// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

import {IHPRewardsErrors} from "./IHPRewardsErrors.sol";
import {IHPRewardsStorage} from "./IHPRewardsStorage.sol";

interface IHPRewards is IHPRewardsErrors, IHPRewardsStorage {
    /// @dev Emitted when the HPRewards contract is initialized
    /// @param hpRewardClaimDelayInSeconds The HP reward claim delay in seconds
    event HPRewardsInitialized(uint256 indexed hpRewardClaimDelayInSeconds);

    /// @dev Emitted when the HPRewards contract is initialized in version 2
    event HPRewardsInitializedV2();

    /// @dev Emitted when the HPRewards contract is initialized in version 3
    event HPRewardsInitializedV3();

    /// @dev Emitted when the capacity rewards are committed
    /// @param regionId The region ID
    /// @param hwClass The hardware class
    /// @param checkPointIncrease The increase in the checkpoint
    /// @param newCheckPoint The new checkpoint
    event CapacityRewardsCommitted(string regionId, string hwClass, uint256 checkPointIncrease, uint256 newCheckPoint);

    /// @dev Emitted when the HP reward claim delay is set
    /// @param newHpRewardClaimDelayInSeconds The new HP reward claim delay in seconds
    event HpRewardClaimDelaySet(uint256 indexed newHpRewardClaimDelayInSeconds);

    /// @dev Emitted when a HP reward claim is initiated
    /// @param scalerNodeId The scaler node ID
    /// @param totalCapacityReward The total capacity reward
    /// @param totalUtilizationReward The total utilization reward
    /// @param delegatorShare The delegator share
    /// @param timestamp The timestamp
    /// @param claimIndex The claim index
    /// @param hp The HP address
    event HpRewardClaimInitiated(
        uint256 indexed scalerNodeId,
        uint256 totalCapacityReward,
        uint256 totalUtilizationReward,
        uint256 delegatorShare,
        uint256 timestamp,
        uint256 indexed claimIndex,
        address indexed hp
    );

    /// @dev Emitted when a HP reward claim is initiated
    /// @param scalerNodeId The scaler node ID
    /// @param claimIndex The claim index
    /// @param hp The HP address
    /// @param totalCapacityReward The total capacity reward
    /// @param totalUtilizationReward The total utilization reward
    /// @param delegatorShare The delegator share
    /// @param timestamp The timestamp
    /// @param unclaimedRewards The unclaimed rewards
    event HpRewardClaimInitiatedV2(
        uint256 indexed scalerNodeId,
        uint256 indexed claimIndex,
        address indexed hp,
        uint256 totalCapacityReward,
        uint256 totalUtilizationReward,
        uint256 delegatorShare,
        uint256 timestamp,
        uint256 unclaimedRewards
    );

    /// @dev Emitted when a HP reward batch claim is initiated
    /// @param scalerNodeIds The scaler node IDs array
    /// @param claimIndex The claim index
    /// @param hp The HP address
    /// @param totalCapacityReward The total capacity reward
    /// @param totalUtilizationReward The total utilization reward
    /// @param delegatorShare The delegator share
    /// @param timestamp The timestamp
    /// @param unclaimedRewards The total unclaimed rewards
    event BatchHpRewardClaimInitiated(
        uint256[] scalerNodeIds,
        uint256 indexed claimIndex,
        address indexed hp,
        uint256 totalCapacityReward,
        uint256 totalUtilizationReward,
        uint256 delegatorShare,
        uint256 timestamp,
        uint256 unclaimedRewards
    );

    /// @dev Emitted when a HP reward claim is claimed
    /// @param hp The HP address
    /// @param amount The amount
    /// @param claimIndex The claim index
    event HpRewardClaimed(address indexed hp, uint256 indexed amount, uint256 indexed claimIndex);

    /// @dev Emitted when a HP reward claim is settled
    /// @param scalerNodeId The scaler node ID
    /// @param totalCapacityReward The total capacity reward
    /// @param totalUtilizationReward The total utilization reward
    /// @param delegatorShare The delegator share
    event HpRewardsSettled(
        uint256 indexed scalerNodeId, uint256 totalCapacityReward, uint256 totalUtilizationReward, uint256 delegatorShare
    );

    /// @dev Emitted when the network collateral reward redirection ratio is set
    /// @param newNetworkCollateralRewardRedirectionRatio The new network collateral reward redirection ratio
    event NetworkCollateralRewardRedirectionRatioSet(uint256 indexed newNetworkCollateralRewardRedirectionRatio);

    /// @dev Emitted when the ICNT unlocking start timestamp is set
    /// @param newICNTUnlockStartTimestamp The new ICNT unlocking start timestamp
    event ICNTUnlockStartTimestampSet(uint256 indexed newICNTUnlockStartTimestamp);

    /// @dev Emitted when the unlocked ICNT by month is set
    /// @param newUnlockedICNTByMonth The new unlocked ICNT by month
    event UnlockedICNTByMonthSet(uint256[] indexed newUnlockedICNTByMonth);

    /// @dev Emitted when the unlocked ICNT by month is set
    /// @param newUnlockedICNTByMonthIndexed The new unlocked ICNT by month indexed
    /// @param newUnlockedICNTByMonthUnindexed The new unlocked ICNT by month unindexed
    event UnlockedICNTByMonthSetV2(uint256[] indexed newUnlockedICNTByMonthIndexed, uint256[] newUnlockedICNTByMonthUnindexed);

    /// @dev Emitted when the node collateral is increased from available rewards
    /// @param scalerNodeId The scaler node ID
    /// @param collateralAmount The collateral amount
    event NodeCollateralIncreasedFromAvailableRewards(uint256 indexed scalerNodeId, uint256 collateralAmount);

    /// @dev Emitted when the network collateral is increased from available rewards
    /// @param networkCollateral The network collateral
    event NetworkCollateralIncreasedFromAvailableRewards(uint256 indexed scalerNodeId, uint256 networkCollateral);

    /// @dev Emitted when the HP rewards are activated
    event HpRewardsActivated();

    /// @notice Initializes the HPRewards contract.
    /// @param _rewardClaimDelayInSeconds The delay in seconds before a HP can claim its rewards.
    /// @param _networkCollateralRewardRedirectionRatio The network collateral reward redirection ratio.
    /// @param _icntUnlockStartTimestamp The timestamp when ICNT unlocking starts.
    /// @param _lockedICNTByMonth The unlocked ICNT by month.
    /// @param regionIds List of regionIds to commit rewards
    /// @param hwClassIds List of hwClassIds to commit rewards
    function initializeHPRewards(
        uint256 _rewardClaimDelayInSeconds,
        uint256 _networkCollateralRewardRedirectionRatio,
        uint256 _icntUnlockStartTimestamp,
        uint256[] memory _lockedICNTByMonth,
        string[] memory regionIds,
        string[] memory hwClassIds
    ) external;

    /// @notice Commits the rewards for a given region and hardware class.
    /// @dev Intended to be called by the Protocol contract only.
    /// @param _regionId The region ID.
    /// @param _hwClass The hardware class.
    function commitHpRewards(string calldata _regionId, string calldata _hwClass) external returns (uint256);

    /// @notice Claims the rewards for a given HP.
    /// @dev Intended to be called by the HP contract only.
    /// @param _scalerNodeId The node ID of the HP.
    function initiateHpRewardsClaim(uint256 _scalerNodeId) external;

    /// @notice Initiates the claim of rewards for multiple nodes of the same HP in a batch.
    /// @dev Intended to be called by the HP contract only.
    /// @param _scalerNodeIds The array of node IDs of the HPs.
    function batchInitiateHpRewardsClaim(uint256[] memory _scalerNodeIds) external;

    /// @notice Claims the rewards for a given HP.
    /// @dev Intended to be called by the HP contract only.
    /// @param _claimIndex The index of the claim to be claimed.
    function claimHpRewards(uint256 _claimIndex) external;

    /// @notice Called by the HPDelegationICNT contract to settle the HP's base rewards to the delegators.
    /// @param _scalerNodeId The node ID of the HP.
    function settleHpRewardsDelegatorShare(uint256 _scalerNodeId) external;

    /// @notice Sets the reward claim delay.
    /// @param _rewardClaimDelayInSeconds The delay in seconds before a HP can claim its rewards.
    function setHpRewardClaimDelay(uint256 _rewardClaimDelayInSeconds) external;

    /// @notice Sets the network collateral reward redirection ratio.
    /// @param _networkCollateralRewardRedirectionRatio The network collateral reward redirection ratio.
    function setNetworkCollateralRewardRedirectionRatio(uint256 _networkCollateralRewardRedirectionRatio) external;

    /// @notice Sets the ICNT unlocking start timestamp.
    /// @param _icntUnlockStartTimestamp The timestamp when ICNT unlocking starts.
    function setICNTUnlockStartTimestamp(uint256 _icntUnlockStartTimestamp) external;

    /// @notice Sets the locked ICNT by month.
    /// @param _lockedICNTByMonth The locked ICNT by month.
    function setLockedICNTByMonth(uint256[] memory _lockedICNTByMonth) external;

    /// @notice Activates the HP rewards.
    function activateHpRewards() external;

    /// @notice Returns the unclaimed rewards for a given node.
    /// @param _scalerNodeId The node ID of the HP.
    /// @return nodeClaimableRewards The total claimable rewards for the node, excluding the delegators' share.
    /// @return delegatorRewards The delegators' share of the rewards generated.
    function unclaimedHpRewards(uint256 _scalerNodeId)
        external
        view
        returns (uint256 nodeClaimableRewards, uint256 delegatorRewards);

    /// @notice Returns the unlocked ICNT for a given timestamp.
    /// @param _timestamp The timestamp.
    /// @return The unlocked ICNT.
    function getUnlockedICNT(uint256 _timestamp) external view returns (uint256);

    /// @notice Returns the updated HP delegator reward share accumulation for a given node.
    /// @param _scalerNodeId The node ID of the HP.
    /// @return The updated HP delegator reward share accumulation.
    function getUpdatedHpDelegatorRewardShareAccumulation(uint256 _scalerNodeId) external view returns (uint256);

    /// @notice Returns the reward claim delay.
    /// @return The reward claim delay.
    function getHpRewardClaimDelay() external view returns (uint256);

    /// @notice Returns the network collateral reward redirection ratio.
    /// @return The network collateral reward redirection ratio.
    function getNetworkCollateralRewardRedirectionRatio() external view returns (uint256);

    /// @notice Returns the ICNT unlock start timestamp.
    /// @return The ICNT unlock start timestamp.
    function getICNTUnlockStartTimestamp() external view returns (uint256);

    /// @notice Returns the locked ICNT by month.
    /// @return The locked ICNT by month.
    function getLockedICNTByMonth() external view returns (uint256[] memory);

    /// @notice Returns the version of the HPRewards contract.
    /// @return The version of the HPRewards contract.
    function getHPRewardsVersion() external view returns (uint64);

    /// @notice Returns the reward claims for a given HP.
    /// @param _hp The address of the HP.
    /// @return The reward claims.
    function getHpRewardClaims(address _hp) external view returns (RewardClaim[] memory);
}
