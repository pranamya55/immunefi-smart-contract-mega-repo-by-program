// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {AccessControlDefaultAdminRules} from "@openzeppelin/contracts/access/extensions/AccessControlDefaultAdminRules.sol";
import {Pausable} from "@openzeppelin/contracts/utils/Pausable.sol";
import {ISimpleToken} from "./interfaces/ISimpleToken.sol";
import {IRewardDistributor} from "./interfaces/IRewardDistributor.sol";
import {IERC20Rebasing} from "./interfaces/IERC20Rebasing.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract RewardDistributor is IRewardDistributor, AccessControlDefaultAdminRules, Pausable {
    using SafeERC20 for IERC20;

    bytes32 public constant SERVICE_ROLE = keccak256("SERVICE_ROLE");
    bytes32 public constant REWARD_DRIPPER_ROLE = keccak256("REWARD_DRIPPER_ROLE");

    uint256 public constant DRIP_DURATION = 86_400;

    address public immutable ST_USR_ADDRESS;
    address public immutable TOKEN_ADDRESS;
    address public feeCollectorAddress;

    Drip public drip;

    mapping(bytes32 => bool) private rewardAllocationIds;

    modifier idempotent(bytes32 idempotencyKey) {
        if (rewardAllocationIds[idempotencyKey]) {
            revert IdempotencyKeyAlreadyExist(idempotencyKey);
        }
        _;
        rewardAllocationIds[idempotencyKey] = true;
    }

    constructor(
        address _stUSRAddress,
        address _feeCollectorAddress,
        address _tokenAddress
    ) AccessControlDefaultAdminRules(1 days, msg.sender) {
        require(_stUSRAddress != address(0), ZeroAddress());
        require(_feeCollectorAddress != address(0), ZeroAddress());
        require(_tokenAddress != address(0), ZeroAddress());

        ST_USR_ADDRESS = _stUSRAddress;
        feeCollectorAddress = _feeCollectorAddress;
        TOKEN_ADDRESS = _tokenAddress;
    }

    function allocateReward(
        bytes32 _idempotencyKey,
        uint256 _stakingReward,
        uint256 _feeReward
    ) external onlyRole(SERVICE_ROLE) idempotent(_idempotencyKey) whenNotPaused {
        require(_stakingReward > 0, InvalidAmount(_stakingReward));
        dripReward(true, _stakingReward);
        IERC20Rebasing stUSR = IERC20Rebasing(ST_USR_ADDRESS);
        uint256 totalShares = stUSR.totalShares();
        uint256 totalUSRBefore = stUSR.totalSupply();

        ISimpleToken token = ISimpleToken(TOKEN_ADDRESS);
        token.mint(address(this), _stakingReward);
        token.mint(feeCollectorAddress, _feeReward);

        uint256 totalUSRAfter = totalUSRBefore + _stakingReward;
        
        emit RewardAllocated(
            _idempotencyKey,
            totalShares,
            totalUSRBefore,
            totalUSRAfter,
            _stakingReward,
            _feeReward
        );
    }

    function dripReward() external onlyRole(REWARD_DRIPPER_ROLE) whenNotPaused() {
        dripReward(false, drip.stakingReward);
    }

    function emergencyWithdrawERC20(
        IERC20 _token,
        address _to,
        uint256 _amount
    ) external onlyRole(DEFAULT_ADMIN_ROLE) {
        require(address(_token) != address(0), ZeroAddress());
        require(address(_to) != address(0), ZeroAddress());
        require(_amount != 0, InvalidAmount(_amount));

        _token.safeTransfer(_to, _amount);

        emit EmergencyWithdrawnERC20(address(_token), _to, _amount);
    }

    function setFeeCollector(address _feeCollectorAddress) external onlyRole(DEFAULT_ADMIN_ROLE) {
        require(_feeCollectorAddress != address(0), ZeroAddress());
        feeCollectorAddress = _feeCollectorAddress;

        emit FeeCollectorSet(_feeCollectorAddress);
    }

    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        Pausable._pause();
    }

    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        Pausable._unpause();
    }


    function availableFunds() public view returns (uint256) {
        uint256 balance = IERC20(TOKEN_ADDRESS).balanceOf(address(this));
        uint256 elapsed = block.timestamp - drip.lastCollect;
        uint256 allowed = elapsed * drip.stakingReward / DRIP_DURATION;
        return (allowed > balance) ? balance : allowed;
    }

    function dripReward(bool _isNewAllocation, uint256 _stakingReward) internal {
        if (_isNewAllocation || _stakingReward < DRIP_DURATION) {
            uint256 balance = IERC20(TOKEN_ADDRESS).balanceOf(address(this));
            if (balance > 0) {
                IERC20(TOKEN_ADDRESS).safeTransfer(ST_USR_ADDRESS, balance);
            }
            drip.stakingReward = _stakingReward;
            drip.lastCollect = block.timestamp;
            emit RewardDripped(balance);
            return;
        }

        uint256 toSend = availableFunds();
        if (toSend > 0) {
            drip.lastCollect = block.timestamp;
            IERC20(TOKEN_ADDRESS).safeTransfer(ST_USR_ADDRESS, toSend);
        }

        emit RewardDripped(toSend);
    }

}
