// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

/// @title ProtocolConstants
/// @notice Contains protocol-level default values.
library ProtocolConstants {
    /// @notice One month is equal to 30 days
    uint256 public constant ONE_MONTH = 30 days;
    /// @notice One year is equal to 12 * ONE_MONTH
    uint256 public constant ONE_YEAR = 12 * ONE_MONTH;
    /// @notice The default maximum number of staked links per hyper node.
    uint256 public constant DEFAULT_MAX_LINKS_PER_HN = 400;
    /// @notice The default maximum number of staked links per scaler node.
    uint256 public constant DEFAULT_MAX_LINKS_PER_SN = 2000;
    /// @notice The default precision for all calculations.
    uint256 public constant DEFAULT_PRECISION = 1e18;
    /// @notice Constant used in percentage calculations.
    uint256 public constant ONE_HUNDRED_PERCENT = 100 * DEFAULT_PRECISION;
    /// @notice The minimum percentage of collateral to provide at node registration.
    uint256 public constant DEFAULT_MINIMUM_COLLATERAL_PERCENT = 30 * DEFAULT_PRECISION;
    /// @notice The maximum number of nodes registered on a cluster.
    uint256 public constant DEFAULT_MAX_NODES_PER_CLUSTER = 50;
    /// @notice The total supply of ICNT.
    uint256 public constant ICNT_TOTAL_SUPPLY = 700000000 * 10 ** 18;
    /// @notice The unit of time for the delegator ICNT locking period.
    ///         All ICNT locking periods are a multiple of this unit.
    uint256 public constant DELEGATOR_ICNT_LOCKING_PERIOD_UNIT = 1 days;
    /// @notice The minimum amount of time a delegator must lock their ICNT for,
    ///         applicable ONLY when immediately locking accrued rewards
    uint256 public constant MIN_DELEGATOR_ICNT_REWARDS_LOCK_TIME_IN_SECONDS = 1 days;
    /// @notice The maximum amount of time a delegator can lock their ICNT for.
    uint256 public constant MAX_DELEGATOR_ICNT_LOCK_TIME_IN_SECONDS = 48 * ONE_MONTH;
    /// @notice The maximum minimum staking period for a link.
    uint256 public constant MAX_MIN_LINK_STAKING_PERIOD_IN_SECONDS = 6 * ONE_MONTH;
    /// @notice The maximum unstaking period for a link.
    uint256 public constant MAX_LINK_UNSTAKING_PERIOD_IN_ERAS = 175;
    /// @notice The maximum number of links that can be staked at once
    uint256 public constant MAX_LINK_STAKE_COUNT = 100;
    /// @notice Minimum collateral commitment duration when registering a Node
    uint256 public constant MIN_COMMITMENT_DURATION = 36 * ONE_MONTH;
    /// @notice The release schedule duration for capacity rewards
    uint256 public constant RELEASE_SCHEDULE_DURATION = 4 * ONE_YEAR; // 4 years
    /// @notice The number of Eras required to be waited before unstaking collateral post unstake initiation
    uint256 public constant DEFAULT_UNSTAKE_DELAY_AFTER_INITIATION_IN_ERAS = 2;
    /// @notice The total rewards pool for NFT rewards
    uint256 public constant TOTAL_NFT_REWARDS_POOL = 140000000;
    /// @notice The total number of NFT tokens
    uint256 public constant TOTAL_NFT_TOKENS = 55000;
    /// @notice The total number of unsold NFT tokens
    uint256 public constant TOTAL_NFT_UNSOLD = 25000;
    /// @notice The maximum reward curve
    uint256 public constant MAX_REWARD_CURVE = DEFAULT_PRECISION;
    /// @notice The minimum wait period for claims withdrawal
    uint256 public constant MIN_WAIT_PERIOD_FOR_CLAIMS_WITHDRAWAL = 3 * ONE_MONTH;
    /// @notice The maximum minimum wait period for claims withdrawal
    uint256 public constant MAX_MIN_WAIT_PERIOD_FOR_CLAIMS_WITHDRAWAL = ONE_YEAR;
    /// @notice The initial reward distribution
    uint256 public constant INITIAL_REWARD_DISTRIBUTION = 381.8181818181818 * (10 ** 18); //0.15*140000000/55000
    /// @notice The reward curve length, 48
    /// + 1 occurence for first index initial reward distribution
    /// + 1 occurence for last value duplication
    uint256 public constant REWARD_CURVE_LENGTH = 50;
    /// @notice Delegator Scaling Factor Default Parameters
    uint256 public constant DELEGATOR_SCALING_FACTOR_DEFAULT_C1 = 153;
    uint256 public constant DELEGATOR_SCALING_FACTOR_DEFAULT_C2 = 925;
    uint256 public constant DELEGATOR_SCALING_FACTOR_DEFAULT_C3 = 950;
    /// @notice Node reward share cannot exceed 100%
    uint256 public constant MAX_NODE_REWARD_SHARE = DEFAULT_PRECISION;
    /// @notice Network collateral reward redirection ration cannot exceed 100%
    uint256 public constant MAX_NETWORK_REDIRECTION_RATION = DEFAULT_PRECISION;
    /// @notice Minimum marketAdjustementFactor value
    uint256 public constant MIN_MARKET_ADJUSTMENT_FACTOR = 1e16;
    /// @notice Maximum number of claims that can be delegated at once
    uint256 public constant MAX_CLAIM_TO_DELEGATE = 1000;
    /// @notice Maximum number of claims that can be multi-claimed at once
    uint256 public constant MAX_ICNL_STAKES_TO_MULTI_CLAIM = 1000;
    /// @notice Maximum number of scaler nodes that can be registered in a single batch operation
    uint256 public constant MAX_SCALER_NODES_BATCH_REGISTER = 1000;
    /// @notice Maximum number of scaler nodes that can be updated in a single batch operation
    uint256 public constant MAX_SCALER_NODES_BATCH_UPDATE = 1000;
    /// @notice Maximum number of scaler nodes that can be claimed in a single batch operation
    uint256 public constant MAX_SCALER_NODES_BATCH_CLAIM = 300;
    /// @notice Default protocol margin for hardware classes
    uint256 public constant DEFAULT_PROTOCOL_MARGIN = 25e16; // 25% default protocol margin
}
