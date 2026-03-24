// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {IDefaultErrors} from "./IDefaultErrors.sol";

interface IRewardDistributor is IDefaultErrors {

    struct Drip {
        uint256 lastCollect;
        uint256 stakingReward;
    }

    event RewardAllocated(
        bytes32 indexed _idempotencyKey,
        uint256 _totalShares,
        uint256 _totalUSRBefore,
        uint256 _totalUSRAfter,
        uint256 _stakingReward,
        uint256 _feeReward
    );
    event FeeCollectorSet(address _feeCollector);
    event RewardDripped(uint256 _amount);
    event EmergencyWithdrawnERC20(address indexed _token, address indexed _to, uint256 _amount);

    function allocateReward(bytes32 _idempotencyKey, uint256 _stakingReward, uint256 _feeReward) external;

    function dripReward() external;

    function setFeeCollector(address _feeCollectorAddress) external;

    function pause() external;

    function unpause() external;

    function emergencyWithdrawERC20(
        IERC20 _token,
        address _to,
        uint256 _amount
    ) external;

    function availableFunds() external view returns (uint256);

}
