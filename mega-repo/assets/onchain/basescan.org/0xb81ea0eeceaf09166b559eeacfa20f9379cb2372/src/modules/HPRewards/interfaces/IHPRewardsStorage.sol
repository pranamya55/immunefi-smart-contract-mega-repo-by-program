// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

interface IHPRewardsStorage {
    struct ScalerNodeData {
        uint256 rewardDebt;
        uint256 capacityRewardCheckpoint;
        uint256 lastUtilizationRewardClaimedTimestamp;
    }

    struct RewardClaim {
        uint256 amount;
        uint256 timestamp;
    }
}
