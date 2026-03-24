// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

import {IHPRewardsStorage} from "./interfaces/IHPRewardsStorage.sol";

contract HPRewardsStorage is IHPRewardsStorage {
    /// @custom:storage-location erc7201:hprewards.storage
    struct HPRewardsStorageData {
        uint64 version;
        uint256 rewardsActivationTimestamp;
        uint256 rewardClaimDelayInSeconds;
        uint256 networkCollateralRewardRedirectionRatio;
        uint256 icntUnlockStartTimestamp;
        uint256[] lockedICNTByMonth;
        // Capacity rewards global state
        mapping(string regionId => mapping(string hwClass => uint256 lastUpdatedTimestamp)) lastUpdatedTimestamp;
        mapping(string regionId => mapping(string hwClass => uint256 capacityRewardCheckpoint)) capacityRewardCheckpoint;
        // Per node state
        mapping(uint256 scalerNodeId => ScalerNodeData scalerNodeData) scalerNodeData;
        mapping(address hpId => RewardClaim[]) rewardClaims;
    }

    // keccak256(abi.encode(uint256(keccak256("hprewards.storage")) - 1)) & ~bytes32(uint256(0xff));
    bytes32 internal constant HP_REWARDS_STORAGE_SLOT = 0x5dc66b3e673fa89266368de5b996a274f5f7dd6a9ce3b8224e67db19f11e1e00;

    function _initializeHwClassRewards(string memory _regionId, string memory _hwClass) internal {
        HPRewardsStorageData storage hs = getHPRewardsStorage();
        hs.lastUpdatedTimestamp[_regionId][_hwClass] = block.timestamp;
        hs.capacityRewardCheckpoint[_regionId][_hwClass] = 0;
    }

    /// @dev Must be called post _commitRewards
    function _initializeScalerNodeRewards(uint256 _scalerNodeId, string memory _regionId, string memory _hwClass) internal {
        HPRewardsStorageData storage hs = getHPRewardsStorage();
        hs.scalerNodeData[_scalerNodeId] = ScalerNodeData({
            rewardDebt: 0,
            capacityRewardCheckpoint: hs.capacityRewardCheckpoint[_regionId][_hwClass],
            lastUtilizationRewardClaimedTimestamp: block.timestamp
        });
    }

    function _createHpRewardClaim(address _hpId, uint256 _amount) internal returns (RewardClaim storage claim, uint256 index) {
        HPRewardsStorageData storage hs = getHPRewardsStorage();

        uint256 claimUnlockTimestamp = block.timestamp + hs.rewardClaimDelayInSeconds;
        hs.rewardClaims[_hpId].push(RewardClaim({amount: _amount, timestamp: claimUnlockTimestamp}));

        claim = hs.rewardClaims[_hpId][hs.rewardClaims[_hpId].length - 1];
        index = hs.rewardClaims[_hpId].length - 1;
    }

    function getHPRewardsStorage() internal pure returns (HPRewardsStorageData storage ms) {
        bytes32 slot = HP_REWARDS_STORAGE_SLOT;
        assembly {
            ms.slot := slot
        }
    }
}
