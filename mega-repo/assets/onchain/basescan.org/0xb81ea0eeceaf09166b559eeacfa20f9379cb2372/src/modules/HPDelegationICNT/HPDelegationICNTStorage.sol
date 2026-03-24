// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

import {IHPDelegationICNTStorage} from "./interfaces/IHPDelegationICNTStorage.sol";
import {ProtocolConstants} from "../../common/ProtocolConstants.sol";

contract HPDelegationICNTStorage is IHPDelegationICNTStorage {
    /// @custom:storage-location erc7201:hpdelegationcnt.storage
    struct HPDelegationICNTStorageData {
        uint64 version;
        bool rewardsActivated;
        /// Parameters
        uint256 allowUnstakeDelayAfterStakingInSeconds;
        uint256 allowReclaimDelayAfterUnstakeInEras;
        uint256 allowRewardClaimDelayAfterStakingInSeconds;
        uint256 scalingFactorC1;
        uint256 scalingFactorC2;
        uint256 scalingFactorC3;
        uint256[] maxApyCurve;
        // Staked ICNT State
        uint256 totalDelegatedICNT;
        mapping(uint256 nodeId => uint256 totalDelegatedICNT) nodeTotalDelegatedICNT;
        mapping(address delegator => UserDelegation[] positions) delegations;
        mapping(address delegator => PendingUserRewardClaims[] pendingRewardClaims) pendingRewardClaims;
        // Reward State
        uint256 lastRewardCommitmentTimestamp;
        // Delegator Base Incentive Accumulation
        uint256 delegatorBaseIncentiveAccumulation;
        // Delegator Node Reward Share Accumulation
        mapping(uint256 nodeId => uint256 accumulationPerICNT) nodeRewardAccumulationPerICNT;
    }

    // keccak256(abi.encode(uint256(keccak256("hpdelegationcnt.storage")) - 1)) & ~bytes32(uint256(0xff));
    bytes32 internal constant HP_DELEGATION_ICNT_STORAGE_SLOT = 0x86284dd90e18a3083f5174fbac7645faf9a1f193a5535c362180782092a3ff00;

    function _addNodeRewardShareForDelegators(uint256 _nodeId, uint256 _icntAmount) internal returns (bool hasDelegation) {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();

        if (ds.nodeTotalDelegatedICNT[_nodeId] == 0) {
            return false;
        }

        hasDelegation = true;

        uint256 newNodeRewardShareAccumulationPerICNT = _calculateNewNodeRewardShareAccumulationPerICNT(_nodeId, _icntAmount);

        ds.nodeRewardAccumulationPerICNT[_nodeId] = newNodeRewardShareAccumulationPerICNT;

        emit NodeRewardAccumulationPerICNTCheckpointUpdated(_nodeId, _icntAmount, newNodeRewardShareAccumulationPerICNT);
    }

    function _calculateNewNodeRewardShareAccumulationPerICNT(uint256 _nodeId, uint256 _icntAmount)
        internal
        view
        returns (uint256)
    {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        uint256 nodeTotalDelegatedICNT_ = ds.nodeTotalDelegatedICNT[_nodeId];
        if (nodeTotalDelegatedICNT_ == 0) {
            return ds.nodeRewardAccumulationPerICNT[_nodeId];
        }
        return ds.nodeRewardAccumulationPerICNT[_nodeId]
            + (_icntAmount * ProtocolConstants.DEFAULT_PRECISION) / nodeTotalDelegatedICNT_;
    }

    function getHPDelegationICNTStorage() internal pure returns (HPDelegationICNTStorageData storage ms) {
        bytes32 slot = HP_DELEGATION_ICNT_STORAGE_SLOT;
        assembly {
            ms.slot := slot
        }
    }
}
