// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

interface IHPDelegationICNTStorage {
    /// @notice User delegation data - an instance of this data is created whenever a user locks their ICNT
    struct UserDelegation {
        // The amount of ICNT available to withdraw (after unlockTimestamp) OR re-delegate
        uint256 availableLockedTokens;
        // The APY scaling factor for the delegation, dependent on the locking duration
        uint256 apyScalingFactor;
        // The timestamp when the ICNT delegation will be available to withdraw
        uint256 unlockTimestamp;
        // The state of individual network collateral delegations
        NodeDelegation[] nodeDelegations;
    }

    /// @notice An instance of this data is created whenever a certain user delegates their ICNT to a specific node
    struct NodeDelegation {
        // The nodeId to which the ICNT is delegated
        uint256 nodeId;
        // The amount of ICNT delegated
        uint256 amount;
        // The timestamp when the node can undelegate the collateral
        uint256 undelegationAllowedAfterTimestamp;
        // The era post which the node can reclaim the undelegated collateral
        // Initially 0, which means that the delegation is not "undelegated" yet
        // and collateral cannot be reclaimed
        uint256 reclaimAllowedAfterEra;
        // The base APY reward accumulation checkpoints
        uint256 delegatorBaseIncentiveAccumulationCheckpoint;
        // The node reward share accumulation checkpoints
        uint256 nodeRewardAccumulationPerICNTCheckpoint;
    }

    /// @notice A list of pending reward claims for a user
    struct PendingUserRewardClaims {
        // The amount of ICNT to be claimed
        uint256 amount;
        // The timestamp when the reward claim will be available
        uint256 unlockTimestamp;
    }

    event NodeRewardAccumulationPerICNTCheckpointUpdated(
        uint256 indexed nodeId, uint256 indexed amountAdded, uint256 indexed newAccumulationPerICNT
    );
}
