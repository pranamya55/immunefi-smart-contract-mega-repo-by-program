// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {IHPDelegationICNT} from "./interfaces/IHPDelegationICNT.sol";
import {HPDelegationICNTStorage} from "./HPDelegationICNTStorage.sol";
import {ExternalContractManagerStorage} from "../ExternalContractManager/ExternalContractManagerStorage.sol";
import {AccessControlStorage} from "../AccessControl/AccessControlStorage.sol";
import {HPRewardsStorage} from "../HPRewards/HPRewardsStorage.sol";
import {ProtocolConstants} from "src/common/ProtocolConstants.sol";
import {ICNRegistryStorage} from "../ICNRegistry/ICNRegistryStorage.sol";
import {IICNRegistryErrors} from "../ICNRegistry/interfaces/IICNRegistryErrors.sol";
import {IHPRewards} from "../HPRewards/interfaces/IHPRewards.sol";

contract HPDelegationICNT is
    IHPDelegationICNT,
    HPDelegationICNTStorage,
    ExternalContractManagerStorage,
    AccessControlStorage,
    HPRewardsStorage,
    ICNRegistryStorage
{
    using SafeERC20 for IERC20;

    uint256 private constant M = ProtocolConstants.DEFAULT_PRECISION;
    int256 private constant IM = int256(ProtocolConstants.DEFAULT_PRECISION);
    uint256 private constant BASELINE_SCALING_FACTOR_DEN = (
        (
            ProtocolConstants.DELEGATOR_SCALING_FACTOR_DEFAULT_C1 * ProtocolConstants.MAX_DELEGATOR_ICNT_LOCK_TIME_IN_SECONDS
                + ProtocolConstants.DELEGATOR_SCALING_FACTOR_DEFAULT_C2 * 1 days
        ) * M
    )
        / (ProtocolConstants.MAX_DELEGATOR_ICNT_LOCK_TIME_IN_SECONDS + ProtocolConstants.DELEGATOR_SCALING_FACTOR_DEFAULT_C3 * 1 days);

    modifier onlyVerifiedNode(uint256 _nodeId) {
        require(
            getICNRegistryStorage().scalerNodes[_nodeId].status == ScalerNodeStatus.Validated,
            ScalerNodeMustBeVerifiedForDelegation(_nodeId)
        );
        _;
    }

    modifier validLockupDuration(uint256 _lockingDurationInSeconds) {
        require(
            _lockingDurationInSeconds >= ProtocolConstants.DELEGATOR_ICNT_LOCKING_PERIOD_UNIT
                && _lockingDurationInSeconds % ProtocolConstants.DELEGATOR_ICNT_LOCKING_PERIOD_UNIT == 0
                && _lockingDurationInSeconds <= ProtocolConstants.MAX_DELEGATOR_ICNT_LOCK_TIME_IN_SECONDS,
            LockupDurationNotAllowed(_lockingDurationInSeconds)
        );
        _;
    }

    /// @inheritdoc IHPDelegationICNT
    function initializeHPDelegationICNT(
        uint256[] calldata _maxApyCurve,
        uint256 _allowUnstakeDelayAfterStakingInSeconds,
        uint256 _allowReclaimDelayAfterUnstakeInEras,
        uint256 _allowRewardClaimDelayAfterStakingInSeconds
    ) external override onlySelf {
        HPDelegationICNTStorageData storage $ = getHPDelegationICNTStorage();
        require($.version < 3, HPDelegationICNTAlreadyInitialized());

        if ($.version == 0) {
            $.version = 1;

            _setMaxApyCurve(_maxApyCurve);
            _setAllowUnstakeDelayAfterStakingInSeconds(_allowUnstakeDelayAfterStakingInSeconds);
            _setAllowReclaimDelayAfterUnstakeInEras(_allowReclaimDelayAfterUnstakeInEras);
            _setAllowRewardClaimDelayAfterStakingInSeconds(_allowRewardClaimDelayAfterStakingInSeconds);
            _setScalingFactors(
                ProtocolConstants.DELEGATOR_SCALING_FACTOR_DEFAULT_C1,
                ProtocolConstants.DELEGATOR_SCALING_FACTOR_DEFAULT_C2,
                ProtocolConstants.DELEGATOR_SCALING_FACTOR_DEFAULT_C3
            );

            emit HPDelegationModuleInitialized();
        } else if ($.version == 1) {
            $.version = 2;

            emit HPDelegationICNTModuleInitializedV2();
        } else if ($.version == 2) {
            $.version = 3;

            emit HPDelegationICNTModuleInitializedV3();
        }
    }

    /// @inheritdoc IHPDelegationICNT
    function activateDelegationRewards() external override onlyRole(GOVERNANCE_ROLE) {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();

        require(ds.rewardsActivated == false, HPDelegationRewardsAlreadyActivated());

        ds.rewardsActivated = true;
        ds.lastRewardCommitmentTimestamp = block.timestamp;

        emit HPDelegationRewardsActivated();
    }

    /// @inheritdoc IHPDelegationICNT
    function delegateCollateral(uint256 _nodeId, uint256 _amount, uint256 _lockupDurationInSeconds)
        external
        override
        onlyVerifiedNode(_nodeId)
        validLockupDuration(_lockupDurationInSeconds)
        whenNotPaused
    {
        require(_amount != 0, InvalidAmount(_amount, 1));
        _commitDelegatorIncentiveRewards();
        IHPRewards(address(this)).settleHpRewardsDelegatorShare(_nodeId);

        ExternalContractManagerStorageData storage es = getExternalContractManagerStorage();
        es.icnToken.safeTransferFrom(msg.sender, address(this), _amount);

        _createFreshDelegation(msg.sender, _nodeId, _amount, _lockupDurationInSeconds);
    }

    /// @inheritdoc IHPDelegationICNT
    function delegateLockedCollateral(uint256 _nodeId, uint256 _amount, uint256 _lockedDelegationIndex)
        external
        override
        onlyVerifiedNode(_nodeId)
        whenNotPaused
    {
        require(_amount != 0, InvalidAmount(_amount, 1));
        uint256 baseIncentiveAccumulation = _commitDelegatorIncentiveRewards();
        IHPRewards(address(this)).settleHpRewardsDelegatorShare(_nodeId);

        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        UserDelegation storage userDelegation = _getUserDelegation(msg.sender, _lockedDelegationIndex);

        require(
            userDelegation.availableLockedTokens >= _amount,
            InsufficientUnlockedTokens(userDelegation.availableLockedTokens, _amount)
        );

        // Update user state
        userDelegation.availableLockedTokens -= _amount;
        userDelegation.nodeDelegations.push(
            NodeDelegation({
                nodeId: _nodeId,
                amount: _amount,
                undelegationAllowedAfterTimestamp: block.timestamp + ds.allowUnstakeDelayAfterStakingInSeconds,
                reclaimAllowedAfterEra: 0,
                delegatorBaseIncentiveAccumulationCheckpoint: baseIncentiveAccumulation,
                nodeRewardAccumulationPerICNTCheckpoint: ds.nodeRewardAccumulationPerICNT[_nodeId]
            })
        );

        // Update global state
        ds.nodeTotalDelegatedICNT[_nodeId] += _amount;
        ds.totalDelegatedICNT += _amount;

        emit CollateralDelegated(_nodeId, msg.sender, _amount, userDelegation.apyScalingFactor, userDelegation.unlockTimestamp);
        // Add the locked delegation index to the event
        emit CollateralDelegatedV2(
            _nodeId, _lockedDelegationIndex, msg.sender, userDelegation.apyScalingFactor, userDelegation.unlockTimestamp, _amount
        );
    }

    /// @inheritdoc IHPDelegationICNT
    function delegateCollateralFromNodeRewards(
        uint256 _nodeId,
        uint256 _amount,
        address _delegator,
        uint256 _lockupDurationInSeconds
    ) external override onlySelf validLockupDuration(_lockupDurationInSeconds) {
        _commitDelegatorIncentiveRewards();

        _createFreshDelegation(_delegator, _nodeId, _amount, _lockupDurationInSeconds);
    }

    /// @inheritdoc IHPDelegationICNT
    function delegateCollateralFromLinkRewards(
        uint256 _nodeId,
        uint256 _amount,
        address _delegator,
        uint256 _lockupDurationInSeconds
    ) external override onlySelf onlyVerifiedNode(_nodeId) validLockupDuration(_lockupDurationInSeconds) {
        _commitDelegatorIncentiveRewards();
        IHPRewards(address(this)).settleHpRewardsDelegatorShare(_nodeId);

        getExternalContractManagerStorage().reserve.withdraw(address(this), _amount);

        _createFreshDelegation(_delegator, _nodeId, _amount, _lockupDurationInSeconds);
    }

    /// @inheritdoc IHPDelegationICNT
    function undelegateCollateral(uint256 _lockedDelegationIndex, uint256 _nodeDelegationIndex) external override whenNotPaused {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        (UserDelegation storage userDelegation, NodeDelegation storage nodeDelegation) =
            _getUserNodeDelegation(msg.sender, _lockedDelegationIndex, _nodeDelegationIndex);

        // Verify initial conditions
        require(nodeDelegation.reclaimAllowedAfterEra == 0, UndelegationAlreadyInitialized());
        // Check if undelegating is allowed
        require(
            block.timestamp >= nodeDelegation.undelegationAllowedAfterTimestamp,
            AllowUndelegateDelayAfterStakingNotMet(block.timestamp, nodeDelegation.undelegationAllowedAfterTimestamp)
        );

        // Settle any pending rewards
        uint256 baseIncentiveAccumulation = _commitDelegatorIncentiveRewards();
        IHPRewards(address(this)).settleHpRewardsDelegatorShare(nodeDelegation.nodeId);
        uint256 nodeRewardAccumulation = ds.nodeRewardAccumulationPerICNT[nodeDelegation.nodeId];

        // Create a pending claim for any unclaimed rewards
        uint256 _unclaimedRewards = _unclaimedDelegationRewards(
            msg.sender,
            _lockedDelegationIndex,
            _nodeDelegationIndex,
            baseIncentiveAccumulation,
            nodeRewardAccumulation,
            userDelegation,
            nodeDelegation
        );
        if (_unclaimedRewards != 0) {
            uint256 claimIndex = _createPendingRewardsClaim(msg.sender, _unclaimedRewards);

            uint256[] memory lockedDelegationIndexes = new uint256[](1);
            lockedDelegationIndexes[0] = _lockedDelegationIndex;
            uint256[] memory nodeDelegationIndexes = new uint256[](1);
            nodeDelegationIndexes[0] = _nodeDelegationIndex;
            uint256[] memory unclaimedRewards = new uint256[](1);
            unclaimedRewards[0] = _unclaimedRewards;

            emit PendingRewardsClaimed(
                msg.sender,
                lockedDelegationIndexes,
                nodeDelegationIndexes,
                claimIndex,
                unclaimedRewards,
                block.timestamp + ds.allowRewardClaimDelayAfterStakingInSeconds
            );
        }

        // Update local state
        nodeDelegation.reclaimAllowedAfterEra = _getEraManagerCurrentEra() + ds.allowReclaimDelayAfterUnstakeInEras;

        // Update global state
        ds.nodeTotalDelegatedICNT[nodeDelegation.nodeId] -= nodeDelegation.amount;
        ds.totalDelegatedICNT -= nodeDelegation.amount;

        emit CollateralUndelegated(msg.sender, _lockedDelegationIndex, _nodeDelegationIndex);
    }

    /// @inheritdoc IHPDelegationICNT
    function reclaimUndelegatedCollateral(uint256 _lockedDelegationIndex, uint256 _nodeDelegationIndex)
        external
        override
        whenNotPaused
    {
        (UserDelegation storage userDelegation, NodeDelegation storage nodeDelegation) =
            _getUserNodeDelegation(msg.sender, _lockedDelegationIndex, _nodeDelegationIndex);

        // Verify initial conditions
        require(nodeDelegation.reclaimAllowedAfterEra != 0, UnstakingNotInitialized());
        // Check if reclamation is allowed
        uint256 currentEra = _getEraManagerCurrentEra();
        require(
            currentEra >= nodeDelegation.reclaimAllowedAfterEra,
            AllowReclaimDelayAfterInitiationNotMet(currentEra, nodeDelegation.reclaimAllowedAfterEra)
        );

        // Add the previously delegated amount to availableLockedTokens for future delegations
        userDelegation.availableLockedTokens += nodeDelegation.amount;

        // Delete the delegation from the array
        if (userDelegation.nodeDelegations.length > 1 && _nodeDelegationIndex != userDelegation.nodeDelegations.length - 1) {
            userDelegation.nodeDelegations[_nodeDelegationIndex] =
                userDelegation.nodeDelegations[userDelegation.nodeDelegations.length - 1];
        }
        userDelegation.nodeDelegations.pop();

        emit CollateralReclaimed(msg.sender, _lockedDelegationIndex, _nodeDelegationIndex);
    }

    /// @inheritdoc IHPDelegationICNT
    function withdrawUnlockedDelegatedTokens(uint256 _lockedDelegationIndex, uint256 _amount) external override whenNotPaused {
        require(_amount != 0, InvalidAmount(_amount, 1));
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        ExternalContractManagerStorageData storage es = getExternalContractManagerStorage();
        UserDelegation storage userDelegation = _getUserDelegation(msg.sender, _lockedDelegationIndex);

        // Verify initial conditions
        require(block.timestamp >= userDelegation.unlockTimestamp, NotUnlocked(userDelegation.unlockTimestamp));
        require(
            userDelegation.availableLockedTokens >= _amount,
            InsufficientUnlockedTokens(userDelegation.availableLockedTokens, _amount)
        );

        // Update state
        userDelegation.availableLockedTokens -= _amount;
        if (userDelegation.availableLockedTokens == 0 && userDelegation.nodeDelegations.length == 0) {
            // Delete the delegation from the array
            if (ds.delegations[msg.sender].length > 1 && _lockedDelegationIndex != ds.delegations[msg.sender].length - 1) {
                ds.delegations[msg.sender][_lockedDelegationIndex] =
                    ds.delegations[msg.sender][ds.delegations[msg.sender].length - 1];
            }
            ds.delegations[msg.sender].pop();
        }

        // Transfer tokens to the caller
        es.icnToken.safeTransfer(msg.sender, _amount);

        emit UnlockedTokensWithdrawn(msg.sender, _lockedDelegationIndex, _amount);
    }

    /// @inheritdoc IHPDelegationICNT
    function delegateUnclaimedRewards(
        uint256 _lockedDelegationIndex,
        uint256 _nodeDelegationIndex,
        uint256 _nodeId,
        uint256 _lockupDurationInSeconds
    ) external override onlyVerifiedNode(_nodeId) validLockupDuration(_lockupDurationInSeconds) whenNotPaused {
        require(
            _lockupDurationInSeconds >= ProtocolConstants.MIN_DELEGATOR_ICNT_REWARDS_LOCK_TIME_IN_SECONDS,
            LockupDurationNotAllowed(_lockupDurationInSeconds)
        );

        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        ExternalContractManagerStorageData storage es = getExternalContractManagerStorage();
        (UserDelegation storage userDelegation, NodeDelegation storage nodeDelegation) =
            _getUserNodeDelegation(msg.sender, _lockedDelegationIndex, _nodeDelegationIndex);

        uint256 baseIncentiveAccumulation = _commitDelegatorIncentiveRewards();
        IHPRewards(address(this)).settleHpRewardsDelegatorShare(nodeDelegation.nodeId);
        IHPRewards(address(this)).settleHpRewardsDelegatorShare(_nodeId);

        uint256 nodeRewardAccumulation = ds.nodeRewardAccumulationPerICNT[nodeDelegation.nodeId];
        uint256 _unclaimedRewards = _unclaimedDelegationRewards(
            msg.sender,
            _lockedDelegationIndex,
            _nodeDelegationIndex,
            baseIncentiveAccumulation,
            nodeRewardAccumulation,
            userDelegation,
            nodeDelegation
        );

        // Create the delegation
        es.reserve.withdraw(address(this), _unclaimedRewards);
        _createFreshDelegation(msg.sender, _nodeId, _unclaimedRewards, _lockupDurationInSeconds);

        // Update reward accumulation checkpoints
        nodeDelegation.delegatorBaseIncentiveAccumulationCheckpoint = baseIncentiveAccumulation;
        nodeDelegation.nodeRewardAccumulationPerICNTCheckpoint = nodeRewardAccumulation;

        emit RewardsDelegated(msg.sender, _nodeId, _unclaimedRewards, _lockupDurationInSeconds);
    }

    /// @inheritdoc IHPDelegationICNT
    function initiateDelegationRewardsClaim(uint256 _lockedDelegationIndex, uint256 _nodeDelegationIndex)
        external
        override
        whenNotPaused
    {
        uint256 _unclaimedRewards = _initiateDelegationRewardsClaim(
            msg.sender, _lockedDelegationIndex, _nodeDelegationIndex, _commitDelegatorIncentiveRewards()
        );

        uint256 claimIndex = _createPendingRewardsClaim(msg.sender, _unclaimedRewards);

        uint256[] memory lockedDelegationIndexes = new uint256[](1);
        lockedDelegationIndexes[0] = _lockedDelegationIndex;
        uint256[] memory nodeDelegationIndexes = new uint256[](1);
        nodeDelegationIndexes[0] = _nodeDelegationIndex;
        uint256[] memory unclaimedRewards = new uint256[](1);
        unclaimedRewards[0] = _unclaimedRewards;

        emit PendingRewardsClaimed(
            msg.sender,
            lockedDelegationIndexes,
            nodeDelegationIndexes,
            claimIndex,
            unclaimedRewards,
            block.timestamp + getHPDelegationICNTStorage().allowRewardClaimDelayAfterStakingInSeconds
        );
    }

    /// @inheritdoc IHPDelegationICNT
    function batchInitiateDelegationRewardsClaim(
        uint256[] calldata _lockedDelegationIndexes,
        uint256[] calldata _nodeDelegationIndexes
    ) external override whenNotPaused {
        require(
            _lockedDelegationIndexes.length == _nodeDelegationIndexes.length,
            LockedAndNodeDelegationIndexesLengthMismatch(_lockedDelegationIndexes.length, _nodeDelegationIndexes.length)
        );

        HPDelegationICNTStorageData storage $ = getHPDelegationICNTStorage();

        uint256 baseIncentiveAccumulation = _commitDelegatorIncentiveRewards();

        uint256 _unclaimedRewards;
        uint256[] memory unclaimedRewards = new uint256[](_lockedDelegationIndexes.length);
        for (uint256 i = 0; i < _lockedDelegationIndexes.length; i++) {
            uint256 _lockedDelegationIndex = _lockedDelegationIndexes[i];
            uint256 _nodeDelegationIndex = _nodeDelegationIndexes[i];
            require(
                _lockedDelegationIndex < $.delegations[msg.sender].length,
                InvalidLockedDelegationIndex(_lockedDelegationIndex, $.delegations[msg.sender].length)
            );
            require(
                _nodeDelegationIndex < $.delegations[msg.sender][_lockedDelegationIndex].nodeDelegations.length,
                InvalidNodeDelegationIndex(
                    _nodeDelegationIndex, $.delegations[msg.sender][_lockedDelegationIndex].nodeDelegations.length
                )
            );

            uint256 _claimAmount = _initiateDelegationRewardsClaim(
                msg.sender, _lockedDelegationIndex, _nodeDelegationIndex, baseIncentiveAccumulation
            );

            _unclaimedRewards += _claimAmount;
            unclaimedRewards[i] = _claimAmount;
        }

        require(_unclaimedRewards != 0, NoUnclaimedRewards());
        uint256 claimIndex = _createPendingRewardsClaim(msg.sender, _unclaimedRewards);

        emit PendingRewardsClaimed(
            msg.sender,
            _lockedDelegationIndexes,
            _nodeDelegationIndexes,
            claimIndex,
            unclaimedRewards,
            block.timestamp + $.allowRewardClaimDelayAfterStakingInSeconds
        );
    }

    /// @inheritdoc IHPDelegationICNT
    function claimDelegationRewards(uint256 _pendingRewardsClaimIndex) external override whenNotPaused {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        ExternalContractManagerStorageData storage es = getExternalContractManagerStorage();

        PendingUserRewardClaims[] storage pendingRewardsClaims = ds.pendingRewardClaims[msg.sender];
        require(
            _pendingRewardsClaimIndex < pendingRewardsClaims.length,
            InvalidPendingRewardsClaimIndex(_pendingRewardsClaimIndex, pendingRewardsClaims.length)
        );
        PendingUserRewardClaims storage pendingRewardsClaim = pendingRewardsClaims[_pendingRewardsClaimIndex];

        require(block.timestamp >= pendingRewardsClaim.unlockTimestamp, NotUnlocked(pendingRewardsClaim.unlockTimestamp));

        uint256 claimAmount = pendingRewardsClaim.amount;
        es.reserve.withdraw(msg.sender, claimAmount);

        if (pendingRewardsClaims.length > 1 && _pendingRewardsClaimIndex != pendingRewardsClaims.length - 1) {
            pendingRewardsClaims[_pendingRewardsClaimIndex] = pendingRewardsClaims[pendingRewardsClaims.length - 1];
        }
        pendingRewardsClaims.pop();

        emit HPDelegationICNTRewardsClaimed(msg.sender, claimAmount);
        // Add the pending rewards claim index to the event
        emit HPDelegationICNTRewardsClaimedV2(msg.sender, _pendingRewardsClaimIndex, claimAmount);
    }

    /// @inheritdoc IHPDelegationICNT
    function setMaxApyCurve(uint256[] calldata _maxApyCurve) external override onlyRole(TOKENOMICS_ROLE) {
        _commitDelegatorIncentiveRewards();

        _setMaxApyCurve(_maxApyCurve);
    }

    /// @inheritdoc IHPDelegationICNT
    function setAllowUnstakeDelayAfterStakingInSeconds(uint256 _allowUnstakeDelayAfterStakingInSeconds)
        external
        override
        onlyRole(PRODUCT_ROLE)
    {
        _setAllowUnstakeDelayAfterStakingInSeconds(_allowUnstakeDelayAfterStakingInSeconds);
    }

    /// @inheritdoc IHPDelegationICNT
    function setAllowReclaimDelayAfterUnstakeInEras(uint256 _allowReclaimDelayAfterUnstakeInEras)
        external
        override
        onlyRole(PRODUCT_ROLE)
    {
        _setAllowReclaimDelayAfterUnstakeInEras(_allowReclaimDelayAfterUnstakeInEras);
    }

    /// @inheritdoc IHPDelegationICNT
    function setAllowRewardClaimDelayAfterStakingInSeconds(uint256 _allowRewardClaimDelayAfterStakingInSeconds)
        external
        override
        onlyRole(PRODUCT_ROLE)
    {
        _setAllowRewardClaimDelayAfterStakingInSeconds(_allowRewardClaimDelayAfterStakingInSeconds);
    }

    /// @inheritdoc IHPDelegationICNT
    function setScalingFactors(uint256 _scalingFactorC1, uint256 _scalingFactorC2, uint256 _scalingFactorC3)
        external
        override
        onlyRole(TOKENOMICS_ROLE)
    {
        _setScalingFactors(_scalingFactorC1, _scalingFactorC2, _scalingFactorC3);
    }

    /// @inheritdoc IHPDelegationICNT
    function unclaimedDelegationRewards(address delegator, uint256 delegationIndex, uint256 nodeDelegationIndex)
        external
        view
        override
        whenNotPaused
        returns (uint256)
    {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        (,, uint256 baseIncentiveAccumulation) = _getGeneratedRewardFactorsSinceCommit();
        (UserDelegation storage userDelegation, NodeDelegation storage nodeDelegation) =
            _getUserNodeDelegation(delegator, delegationIndex, nodeDelegationIndex);

        uint256 updatedHpDelegatorRewardShareAccumulation =
            IHPRewards(address(this)).getUpdatedHpDelegatorRewardShareAccumulation(nodeDelegation.nodeId);

        return _unclaimedDelegationRewards(
            delegator,
            delegationIndex,
            nodeDelegationIndex,
            ds.delegatorBaseIncentiveAccumulation + baseIncentiveAccumulation,
            updatedHpDelegatorRewardShareAccumulation,
            userDelegation,
            nodeDelegation
        );
    }

    /// @inheritdoc IHPDelegationICNT
    function getTotalDelegatedICNT() external view override returns (uint256) {
        return getHPDelegationICNTStorage().totalDelegatedICNT;
    }

    /// @inheritdoc IHPDelegationICNT
    function getNodeTotalDelegatedICNT(uint256 nodeId) external view override returns (uint256) {
        ICNRegistryStorageData storage rs = getICNRegistryStorage();
        require(rs.scalerNodes[nodeId].status == ScalerNodeStatus.Validated, IICNRegistryErrors.InvalidScalerNode());
        return getHPDelegationICNTStorage().nodeTotalDelegatedICNT[nodeId];
    }

    /// @inheritdoc IHPDelegationICNT
    function getDelegation(address delegator, uint256 index) external view override returns (UserDelegation memory) {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        require(index < ds.delegations[delegator].length, InvalidDelegationIndex(index, ds.delegations[delegator].length));
        return ds.delegations[delegator][index];
    }

    /// @inheritdoc IHPDelegationICNT
    function getDelegations(address delegator) external view override returns (UserDelegation[] memory) {
        return getHPDelegationICNTStorage().delegations[delegator];
    }

    /// @inheritdoc IHPDelegationICNT
    function getPendingDelegatorRewardsClaims(address delegator)
        external
        view
        override
        returns (PendingUserRewardClaims[] memory)
    {
        return getHPDelegationICNTStorage().pendingRewardClaims[delegator];
    }

    function getAllowUnstakeDelayAfterStakingInSeconds() external view override returns (uint256) {
        return getHPDelegationICNTStorage().allowUnstakeDelayAfterStakingInSeconds;
    }

    function getAllowReclaimDelayAfterUnstakeInEras() external view override returns (uint256) {
        return getHPDelegationICNTStorage().allowReclaimDelayAfterUnstakeInEras;
    }

    function getAllowRewardClaimDelayAfterStakingInSeconds() external view override returns (uint256) {
        return getHPDelegationICNTStorage().allowRewardClaimDelayAfterStakingInSeconds;
    }

    /// @inheritdoc IHPDelegationICNT
    function getMaxApyCurve() external view override returns (uint256[] memory) {
        return getHPDelegationICNTStorage().maxApyCurve;
    }

    /// @inheritdoc IHPDelegationICNT
    function getLastRewardCommitmentTimestamp() external view override returns (uint256) {
        return getHPDelegationICNTStorage().lastRewardCommitmentTimestamp;
    }

    /// @inheritdoc IHPDelegationICNT
    function getScalingFactors() external view override returns (uint256, uint256, uint256) {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        return (ds.scalingFactorC1, ds.scalingFactorC2, ds.scalingFactorC3);
    }

    /// @inheritdoc IHPDelegationICNT
    function getHPDelegationICNTVersion() external view returns (uint64) {
        return getHPDelegationICNTStorage().version;
    }

    /// @inheritdoc IHPDelegationICNT
    function calculateScaledApy(uint256 _collateralizationRate, uint256 _lockingDurationInSeconds)
        public
        view
        override
        validLockupDuration(_lockingDurationInSeconds)
        returns (uint256)
    {
        uint256 maxApy = calculateMaxApy(_collateralizationRate);
        uint256 scalingFactor = _calculateApyScalingFactor(_lockingDurationInSeconds);

        return (maxApy * scalingFactor) / M;
    }

    /// @inheritdoc IHPDelegationICNT
    function calculateMaxApy(uint256 _collateralizationRate) public view override returns (uint256) {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();

        uint256 curveLength = ds.maxApyCurve.length;
        if (curveLength == 0) {
            return 0;
        }

        uint256 minX = 0;
        uint256 maxX = M;

        if (_collateralizationRate >= maxX) {
            return ds.maxApyCurve[curveLength - 1];
        }

        if (_collateralizationRate <= minX) {
            return ds.maxApyCurve[0];
        }

        // xSlope = (maxX - minX) / (curveLength - 1);
        uint256 lowIndex = (_collateralizationRate - minX) * (curveLength - 1) / (maxX - minX); // (_cr - minX) / xSlope
        if (((curveLength - 1) * (_collateralizationRate - minX)) % (maxX - minX) == 0) {
            return ds.maxApyCurve[lowIndex];
        }

        int256 lowX = int256(lowIndex * (maxX - minX) / (curveLength - 1) + minX); // lowIndex * xSlope + minX
        int256 lowY = int256(ds.maxApyCurve[lowIndex]);
        int256 highY = int256(ds.maxApyCurve[lowIndex + 1]);
        int256 slope = (highY - lowY) * IM * int256(curveLength - 1) / int256(maxX - minX); // ((highY - lowY) * IM) / xSlope

        int256 value = (lowY * IM + slope * (int256(_collateralizationRate) - lowX)) / IM;

        return uint256(value);
    }

    function _createFreshDelegation(address _delegator, uint256 _nodeId, uint256 _amount, uint256 _lockupDurationInSeconds)
        internal
    {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();

        // Update global state
        ds.nodeTotalDelegatedICNT[_nodeId] += _amount;
        ds.totalDelegatedICNT += _amount;

        // Create a new delegation
        UserDelegation storage userDelegation = ds.delegations[_delegator].push();
        userDelegation.availableLockedTokens = 0;
        userDelegation.apyScalingFactor = _calculateApyScalingFactor(_lockupDurationInSeconds);
        userDelegation.unlockTimestamp = block.timestamp + _lockupDurationInSeconds;
        userDelegation.nodeDelegations.push(
            NodeDelegation({
                nodeId: _nodeId,
                amount: _amount,
                undelegationAllowedAfterTimestamp: block.timestamp + ds.allowUnstakeDelayAfterStakingInSeconds,
                reclaimAllowedAfterEra: 0,
                delegatorBaseIncentiveAccumulationCheckpoint: ds.delegatorBaseIncentiveAccumulation,
                nodeRewardAccumulationPerICNTCheckpoint: ds.nodeRewardAccumulationPerICNT[_nodeId]
            })
        );

        emit CollateralDelegated(
            _nodeId, _delegator, _amount, userDelegation.apyScalingFactor, block.timestamp + _lockupDurationInSeconds
        );
        // Add separate event for delegation creation
        emit DelegationCreated(
            _nodeId,
            _delegator,
            ds.delegations[_delegator].length - 1,
            userDelegation.apyScalingFactor,
            block.timestamp + _lockupDurationInSeconds,
            _amount
        );
    }

    function _initiateDelegationRewardsClaim(
        address _user,
        uint256 _lockedDelegationIndex,
        uint256 _nodeDelegationIndex,
        uint256 _baseIncentiveAccumulation
    ) internal returns (uint256 _unclaimedRewards) {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        (UserDelegation storage userDelegation, NodeDelegation storage nodeDelegation) =
            _getUserNodeDelegation(_user, _lockedDelegationIndex, _nodeDelegationIndex);
        IHPRewards(address(this)).settleHpRewardsDelegatorShare(nodeDelegation.nodeId);

        uint256 nodeRewardAccumulation = ds.nodeRewardAccumulationPerICNT[nodeDelegation.nodeId];
        _unclaimedRewards = _unclaimedDelegationRewards(
            _user,
            _lockedDelegationIndex,
            _nodeDelegationIndex,
            _baseIncentiveAccumulation,
            nodeRewardAccumulation,
            userDelegation,
            nodeDelegation
        );

        require(_unclaimedRewards != 0, NoUnclaimedRewards());

        // Update reward accumulation checkpoints
        nodeDelegation.delegatorBaseIncentiveAccumulationCheckpoint = _baseIncentiveAccumulation;
        nodeDelegation.nodeRewardAccumulationPerICNTCheckpoint = nodeRewardAccumulation;
    }

    function _createPendingRewardsClaim(address _user, uint256 _unclaimedRewards) internal returns (uint256 claimIndex) {
        HPDelegationICNTStorageData storage $ = getHPDelegationICNTStorage();

        // Create a pending reward claim
        uint256 unlockTimestamp = block.timestamp + $.allowRewardClaimDelayAfterStakingInSeconds;
        $.pendingRewardClaims[_user].push(PendingUserRewardClaims({amount: _unclaimedRewards, unlockTimestamp: unlockTimestamp}));
        claimIndex = $.pendingRewardClaims[_user].length - 1;

        emit PendingRewardsClaimInitialized(_user, _unclaimedRewards, unlockTimestamp);
    }

    function _setMaxApyCurve(uint256[] calldata _maxApyCurve) internal {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        require(_maxApyCurve.length != 0, MaxApyCurveShouldHaveAtLeastOnePoint());

        // Delete the existing curve points
        delete ds.maxApyCurve;

        for (uint256 i = 0; i < _maxApyCurve.length; i++) {
            ds.maxApyCurve.push(_maxApyCurve[i]);
        }

        emit MaxApyCurveSet(_maxApyCurve);
    }

    function _commitDelegatorIncentiveRewards() internal returns (uint256) {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();

        (uint256 maxApy, uint256 secondsSinceCommit, uint256 baseIncentiveAccumulation) = _getGeneratedRewardFactorsSinceCommit();
        ds.delegatorBaseIncentiveAccumulation += baseIncentiveAccumulation;
        ds.lastRewardCommitmentTimestamp = block.timestamp;

        emit DelegatorRewardsCommitted(maxApy, secondsSinceCommit, baseIncentiveAccumulation);

        return ds.delegatorBaseIncentiveAccumulation;
    }

    function _setAllowUnstakeDelayAfterStakingInSeconds(uint256 _allowUnstakeDelayAfterStakingInSeconds) internal {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        ds.allowUnstakeDelayAfterStakingInSeconds = _allowUnstakeDelayAfterStakingInSeconds;
        emit AllowUnstakeDelayAfterStakingInSecondsSet(_allowUnstakeDelayAfterStakingInSeconds);
    }

    function _setAllowReclaimDelayAfterUnstakeInEras(uint256 _allowReclaimDelayAfterUnstakeInEras) internal {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        ds.allowReclaimDelayAfterUnstakeInEras = _allowReclaimDelayAfterUnstakeInEras;
        emit AllowReclaimDelayAfterUnstakeInErasSet(_allowReclaimDelayAfterUnstakeInEras);
    }

    function _setAllowRewardClaimDelayAfterStakingInSeconds(uint256 _allowRewardClaimDelayAfterStakingInSeconds) internal {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        ds.allowRewardClaimDelayAfterStakingInSeconds = _allowRewardClaimDelayAfterStakingInSeconds;
        emit AllowRewardClaimDelayAfterStakingInSecondsSet(_allowRewardClaimDelayAfterStakingInSeconds);
    }

    function _setScalingFactors(uint256 _scalingFactorC1, uint256 _scalingFactorC2, uint256 _scalingFactorC3) internal {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        ds.scalingFactorC1 = _scalingFactorC1;
        ds.scalingFactorC2 = _scalingFactorC2;
        ds.scalingFactorC3 = _scalingFactorC3;
        emit ScalingFactorsSet(_scalingFactorC1, _scalingFactorC2, _scalingFactorC3);
    }

    function _currentCollateralizationRate() internal view returns (uint256) {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        return (ds.totalDelegatedICNT * M) / ProtocolConstants.ICNT_TOTAL_SUPPLY;
    }

    function _getGeneratedRewardFactorsSinceCommit()
        internal
        view
        returns (uint256 maxApy, uint256 secondsSinceCommit, uint256 baseIncentiveAccumulation)
    {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        maxApy = calculateMaxApy(_currentCollateralizationRate());
        secondsSinceCommit = block.timestamp - ds.lastRewardCommitmentTimestamp;

        if (!ds.rewardsActivated) {
            baseIncentiveAccumulation = 0;
        } else {
            baseIncentiveAccumulation = (maxApy * secondsSinceCommit) / ProtocolConstants.ONE_YEAR;
        }
    }

    function _unclaimedDelegationRewards(
        address _delegator,
        uint256 _delegationIndex,
        uint256 _nodeDelegationIndex,
        uint256 _delegatorBaseIncentiveAccumulation,
        uint256 _nodeRewardAccumulation,
        UserDelegation storage userDelegation,
        NodeDelegation storage nodeDelegation
    ) internal view returns (uint256 delegationReward) {
        require(
            nodeDelegation.reclaimAllowedAfterEra == 0,
            UndelegatedPositionCannotEarnRewards(_delegator, _delegationIndex, _nodeDelegationIndex)
        );

        uint256 amount = nodeDelegation.amount;

        uint256 baseIncentiveRewards = amount
            * (_delegatorBaseIncentiveAccumulation - nodeDelegation.delegatorBaseIncentiveAccumulationCheckpoint)
            * userDelegation.apyScalingFactor;
        baseIncentiveRewards /= M;

        uint256 nodeReward = ((_nodeRewardAccumulation - nodeDelegation.nodeRewardAccumulationPerICNTCheckpoint) * amount);

        return (baseIncentiveRewards + nodeReward) / M;
    }

    function _calculateApyScalingFactor(uint256 _lockingDurationInSeconds) internal view returns (uint256) {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        uint256 c1 = ds.scalingFactorC1;
        uint256 c2 = ds.scalingFactorC2;
        uint256 c3 = ds.scalingFactorC3;

        uint256 scalingFactorNum =
            ((c1 * _lockingDurationInSeconds + c2 * 1 days) * M) / (_lockingDurationInSeconds + c3 * 1 days);
        uint256 scalingFactorDen = BASELINE_SCALING_FACTOR_DEN;

        return (scalingFactorNum * M) / scalingFactorDen;
    }

    function _getUserDelegation(address _delegator, uint256 _delegationIndex) internal view returns (UserDelegation storage) {
        HPDelegationICNTStorageData storage ds = getHPDelegationICNTStorage();
        require(
            _delegationIndex < ds.delegations[_delegator].length,
            InvalidLockedDelegationIndex(_delegationIndex, ds.delegations[_delegator].length)
        );
        return ds.delegations[_delegator][_delegationIndex];
    }

    function _getUserNodeDelegation(address _delegator, uint256 _delegationIndex, uint256 _nodeDelegationIndex)
        internal
        view
        returns (UserDelegation storage, NodeDelegation storage)
    {
        UserDelegation storage userDelegation = _getUserDelegation(_delegator, _delegationIndex);
        require(
            _nodeDelegationIndex < userDelegation.nodeDelegations.length,
            InvalidNodeDelegationIndex(_nodeDelegationIndex, userDelegation.nodeDelegations.length)
        );
        return (userDelegation, userDelegation.nodeDelegations[_nodeDelegationIndex]);
    }
}
