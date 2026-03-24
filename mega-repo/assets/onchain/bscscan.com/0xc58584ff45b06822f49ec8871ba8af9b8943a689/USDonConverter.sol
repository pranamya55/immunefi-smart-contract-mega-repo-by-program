// SPDX-License-Identifier: BUSL-1.1
pragma solidity 0.8.16;

// contracts/external/chainlink/AggregatorV3Interface.sol

interface AggregatorV3Interface {
  function decimals() external view returns (uint8);

  function description() external view returns (string memory);

  function version() external view returns (uint256);

  function getRoundData(
    uint80 _roundId
  )
    external
    view
    returns (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
    );

  function latestRoundData()
    external
    view
    returns (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
    );
}

// contracts/external/openzeppelin/contracts/token/IERC20.sol

// OpenZeppelin Contracts (last updated v4.5.0) (token/ERC20/IERC20.sol)

/**
 * @dev Interface of the ERC20 standard as defined in the EIP.
 */
interface IERC20 {
  /**
   * @dev Returns the amount of tokens in existence.
   */
  function totalSupply() external view returns (uint256);

  /**
   * @dev Returns the amount of tokens owned by `account`.
   */
  function balanceOf(address account) external view returns (uint256);

  /**
   * @dev Moves `amount` tokens from the caller's account to `to`.
   *
   * Returns a boolean value indicating whether the operation succeeded.
   *
   * Emits a {Transfer} event.
   */
  function transfer(address to, uint256 amount) external returns (bool);

  /**
   * @dev Returns the remaining number of tokens that `spender` will be
   * allowed to spend on behalf of `owner` through {transferFrom}. This is
   * zero by default.
   *
   * This value changes when {approve} or {transferFrom} are called.
   */
  function allowance(address owner, address spender)
    external
    view
    returns (uint256);

  /**
   * @dev Sets `amount` as the allowance of `spender` over the caller's tokens.
   *
   * Returns a boolean value indicating whether the operation succeeded.
   *
   * IMPORTANT: Beware that changing an allowance with this method brings the risk
   * that someone may use both the old and the new allowance by unfortunate
   * transaction ordering. One possible solution to mitigate this race
   * condition is to first reduce the spender's allowance to 0 and set the
   * desired value afterwards:
   * https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
   *
   * Emits an {Approval} event.
   */
  function approve(address spender, uint256 amount) external returns (bool);

  /**
   * @dev Moves `amount` tokens from `from` to `to` using the
   * allowance mechanism. `amount` is then deducted from the caller's
   * allowance.
   *
   * Returns a boolean value indicating whether the operation succeeded.
   *
   * Emits a {Transfer} event.
   */
  function transferFrom(
    address from,
    address to,
    uint256 amount
  ) external returns (bool);

  /**
   * @dev Emitted when `value` tokens are moved from one account (`from`) to
   * another (`to`).
   *
   * Note that `value` may be zero.
   */
  event Transfer(address indexed from, address indexed to, uint256 value);

  /**
   * @dev Emitted when the allowance of a `spender` for an `owner` is set by
   * a call to {approve}. `value` is the new allowance.
   */
  event Approval(address indexed owner, address indexed spender, uint256 value);
}

// contracts/globalMarkets/USDonManager/IUSDonManager.sol

/*
      ▄▄█████████▄
   ╓██▀└ ,╓▄▄▄, '▀██▄
  ██▀ ▄██▀▀╙╙▀▀██▄ └██µ           ,,       ,,      ,     ,,,            ,,,
 ██ ,██¬ ▄████▄  ▀█▄ ╙█▄      ▄███▀▀███▄   ███▄    ██  ███▀▀▀███▄    ▄███▀▀███,
██  ██ ╒█▀'   ╙█▌ ╙█▌ ██     ▐██      ███  █████,  ██  ██▌    └██▌  ██▌     └██▌
██ ▐█▌ ██      ╟█  █▌ ╟█     ██▌      ▐██  ██ └███ ██  ██▌     ╟██ j██       ╟██
╟█  ██ ╙██    ▄█▀ ▐█▌ ██     ╙██      ██▌  ██   ╙████  ██▌    ▄██▀  ██▌     ,██▀
 ██ "██, ╙▀▀███████████⌐      ╙████████▀   ██     ╙██  ███████▀▀     ╙███████▀`
  ██▄ ╙▀██▄▄▄▄▄,,,                ¬─                                    '─¬
   ╙▀██▄ '╙╙╙▀▀▀▀▀▀▀▀
      ╙▀▀██████R⌐
 */

/**
 * @title  IUSDonManager
 * @author Ondo Finance
 * @notice This contract provides an interface for conducting instant USDon swaps.
 */
interface IUSDonManager {
  function subscribe(
    address depositToken,
    uint256 depositAmount,
    uint256 minimumRwaReceived
  ) external returns (uint256 rwaAmountOut);

  function redeem(
    uint256 rwaAmount,
    address receivingToken,
    uint256 minimumTokenReceived
  ) external returns (uint256 receiveTokenAmount);
}

// contracts/external/openzeppelin/contracts/token/IERC20Metadata.sol

// OpenZeppelin Contracts v4.4.1 (token/ERC20/extensions/IERC20Metadata.sol)

/**
 * @dev Interface for the optional metadata functions from the ERC20 standard.
 *
 * _Available since v4.1._
 */
interface IERC20Metadata is IERC20 {
  /**
   * @dev Returns the name of the token.
   */
  function name() external view returns (string memory);

  /**
   * @dev Returns the symbol of the token.
   */
  function symbol() external view returns (string memory);

  /**
   * @dev Returns the decimals places of the token.
   */
  function decimals() external view returns (uint8);
}

// contracts/external/openzeppelin/contracts/token/SafeERC20.sol

// OpenZeppelin Contracts (last updated v5.2.0) (token/ERC20/utils/SafeERC20.sol)

/**
 * @title SafeERC20
 * @dev Wrappers around ERC-20 operations that throw on failure (when the token
 * contract returns false). Tokens that return no value (and instead revert or
 * throw on failure) are also supported, non-reverting calls are assumed to be
 * successful.
 * To use this library you can add a `using SafeERC20 for IERC20;` statement to your contract,
 * which allows you to call the safe operations as `token.safeTransfer(...)`, etc.
 */
library SafeERC20 {
    /**
     * @dev An operation with an ERC-20 token failed.
     */
    error SafeERC20FailedOperation(address token);

    /**
     * @dev Indicates a failed `decreaseAllowance` request.
     */
    error SafeERC20FailedDecreaseAllowance(address spender, uint256 currentAllowance, uint256 requestedDecrease);

    /**
     * @dev Transfer `value` amount of `token` from the calling contract to `to`. If `token` returns no value,
     * non-reverting calls are assumed to be successful.
     */
    function safeTransfer(IERC20 token, address to, uint256 value) internal {
        _callOptionalReturn(token, abi.encodeCall(token.transfer, (to, value)));
    }

    /**
     * @dev Transfer `value` amount of `token` from `from` to `to`, spending the approval given by `from` to the
     * calling contract. If `token` returns no value, non-reverting calls are assumed to be successful.
     */
    function safeTransferFrom(IERC20 token, address from, address to, uint256 value) internal {
        _callOptionalReturn(token, abi.encodeCall(token.transferFrom, (from, to, value)));
    }

    /**
     * @dev Increase the calling contract's allowance toward `spender` by `value`. If `token` returns no value,
     * non-reverting calls are assumed to be successful.
     *
     * IMPORTANT: If the token implements ERC-7674 (ERC-20 with temporary allowance), and if the "client"
     * smart contract uses ERC-7674 to set temporary allowances, then the "client" smart contract should avoid using
     * this function. Performing a {safeIncreaseAllowance} or {safeDecreaseAllowance} operation on a token contract
     * that has a non-zero temporary allowance (for that particular owner-spender) will result in unexpected behavior.
     */
    function safeIncreaseAllowance(IERC20 token, address spender, uint256 value) internal {
        uint256 oldAllowance = token.allowance(address(this), spender);
        forceApprove(token, spender, oldAllowance + value);
    }

    /**
     * @dev Decrease the calling contract's allowance toward `spender` by `requestedDecrease`. If `token` returns no
     * value, non-reverting calls are assumed to be successful.
     *
     * IMPORTANT: If the token implements ERC-7674 (ERC-20 with temporary allowance), and if the "client"
     * smart contract uses ERC-7674 to set temporary allowances, then the "client" smart contract should avoid using
     * this function. Performing a {safeIncreaseAllowance} or {safeDecreaseAllowance} operation on a token contract
     * that has a non-zero temporary allowance (for that particular owner-spender) will result in unexpected behavior.
     */
    function safeDecreaseAllowance(IERC20 token, address spender, uint256 requestedDecrease) internal {
        unchecked {
            uint256 currentAllowance = token.allowance(address(this), spender);
            if (currentAllowance < requestedDecrease) {
                revert SafeERC20FailedDecreaseAllowance(spender, currentAllowance, requestedDecrease);
            }
            forceApprove(token, spender, currentAllowance - requestedDecrease);
        }
    }

    /**
     * @dev Set the calling contract's allowance toward `spender` to `value`. If `token` returns no value,
     * non-reverting calls are assumed to be successful. Meant to be used with tokens that require the approval
     * to be set to zero before setting it to a non-zero value, such as USDT.
     *
     * NOTE: If the token implements ERC-7674, this function will not modify any temporary allowance. This function
     * only sets the "standard" allowance. Any temporary allowance will remain active, in addition to the value being
     * set here.
     */
    function forceApprove(IERC20 token, address spender, uint256 value) internal {
        bytes memory approvalCall = abi.encodeCall(token.approve, (spender, value));

        if (!_callOptionalReturnBool(token, approvalCall)) {
            _callOptionalReturn(token, abi.encodeCall(token.approve, (spender, 0)));
            _callOptionalReturn(token, approvalCall);
        }
    }

    /**
     * @dev Imitates a Solidity high-level call (i.e. a regular function call to a contract), relaxing the requirement
     * on the return value: the return value is optional (but if data is returned, it must not be false).
     * @param token The token targeted by the call.
     * @param data The call data (encoded using abi.encode or one of its variants).
     *
     * This is a variant of {_callOptionalReturnBool} that reverts if call fails to meet the requirements.
     */
    function _callOptionalReturn(IERC20 token, bytes memory data) private {
        uint256 returnSize;
        uint256 returnValue;
        assembly ("memory-safe") {
            let success := call(gas(), token, 0, add(data, 0x20), mload(data), 0, 0x20)
            // bubble errors
            if iszero(success) {
                let ptr := mload(0x40)
                returndatacopy(ptr, 0, returndatasize())
                revert(ptr, returndatasize())
            }
            returnSize := returndatasize()
            returnValue := mload(0)
        }

        if (returnSize == 0 ? address(token).code.length == 0 : returnValue != 1) {
            revert SafeERC20FailedOperation(address(token));
        }
    }

    /**
     * @dev Imitates a Solidity high-level call (i.e. a regular function call to a contract), relaxing the requirement
     * on the return value: the return value is optional (but if data is returned, it must not be false).
     * @param token The token targeted by the call.
     * @param data The call data (encoded using abi.encode or one of its variants).
     *
     * This is a variant of {_callOptionalReturn} that silently catches all reverts and returns a bool instead.
     */
    function _callOptionalReturnBool(IERC20 token, bytes memory data) private returns (bool) {
        bool success;
        uint256 returnSize;
        uint256 returnValue;
        assembly ("memory-safe") {
            success := call(gas(), token, 0, add(data, 0x20), mload(data), 0, 0x20)
            returnSize := returndatasize()
            returnValue := mload(0)
        }
        return success && (returnSize == 0 ? address(token).code.length > 0 : returnValue == 1);
    }
}

// contracts/globalMarkets/USDonManager/USDonConverter.sol

/*
      ▄▄█████████▄
   ╓██▀└ ,╓▄▄▄, '▀██▄
  ██▀ ▄██▀▀╙╙▀▀██▄ └██µ           ,,       ,,      ,     ,,,            ,,,
 ██ ,██¬ ▄████▄  ▀█▄ ╙█▄      ▄███▀▀███▄   ███▄    ██  ███▀▀▀███▄    ▄███▀▀███,
██  ██ ╒█▀'   ╙█▌ ╙█▌ ██     ▐██      ███  █████,  ██  ██▌    └██▌  ██▌     └██▌
██ ▐█▌ ██      ╟█  █▌ ╟█     ██▌      ▐██  ██ └███ ██  ██▌     ╟██ j██       ╟██
╟█  ██ ╙██    ▄█▀ ▐█▌ ██     ╙██      ██▌  ██   ╙████  ██▌    ▄██▀  ██▌     ,██▀
 ██ "██, ╙▀▀███████████⌐      ╙████████▀   ██     ╙██  ███████▀▀     ╙███████▀`
  ██▄ ╙▀██▄▄▄▄▄,,,                ¬─                                    '─¬
   ╙▀██▄ '╙╙╙▀▀▀▀▀▀▀▀
      ╙▀▀██████R⌐
 */

/**
 * @title  USDonConverter
 * @author Ondo Finance
 * @notice This contract manages USDon<>Stablecoin swaps for the GMTokenManager.
 * @dev    This is a basic swap implementation that provides 1:1 swaps between a stablecoin
 *         and USDon (accounting for decimal differences). The contract maintains forward
 *         compatibility by conforming to the IUSDonManager interface for the subscribe
 *         and redeem functions, even though this implementation only supports a single
 *         stablecoin/USDon pair. This design allows for future expansion to support additional
 *         token pairs.
 */
contract USDonConverter is IUSDonManager {
  using SafeERC20 for IERC20;
  // Minimum stablecoin price from Chainlink oracle to allow subscribe/redeem
  uint256 public constant MINIMUM_STABLECOIN_PRICE = 0.98e8; // $0.98 with 8 decimals

  // Maximum oracle data age before being considered outdated
  uint256 public immutable maxOracleDataAge;
  // Normalizer for USDon precision adjustment (1e18)
  uint256 public immutable usdonNormalizer;
  // Normalizer for stablecoin precision adjustment
  uint256 public immutable stablecoinNormalizer;
  /// The GMTokenManager contract authorized to call subscribe/redeem
  address public immutable gmTokenManager;
  /// The wallet that holds both stablecoin and USDon reserves
  address public immutable wallet;
  /// The USDon token
  IERC20 public immutable usdon;
  /// The stablecoin token
  IERC20 public immutable stablecoin;
  /// The stablecoin Chainlink price feed
  AggregatorV3Interface public immutable stablecoinOracle;

  /// Thrown when the stablecoin oracle does not have 8 decimals as assumed
  error InvalidOracleDecimals();
  /// Thrown when attempting to initialize with zero max oracle data age
  error InvalidMaxOracleDataAge();
  /// Thrown when attempting to initialize with zero address
  error ZeroAddress();
  /// Thrown when caller is not the authorized GMTokenManager
  error OnlyGMTokenManager();
  /// Thrown when deposit token is not the set stablecoin
  error InvalidDepositToken();
  /// Thrown when receiving token is not the set stablecoin
  error InvalidReceivingToken();
  /// Thrown when USDon received is below minimum threshold
  error InsufficientUSDonReceived();
  /// Thrown when stablecoin received is below minimum threshold
  error InsufficientStablecoinReceived();
  /// Thrown when oracle price is outdated
  error OraclePriceOutdated();
  /// Thrown when stablecoin price is below minimum threshold
  error StablecoinPriceBelowMinimum();

  /**
   * @notice Constructs the USDonConverter contract
   * @param _gmTokenManager   The GMTokenManager address authorized to call functions
   * @param _wallet           The wallet address that holds token reserves
   * @param _usdon            The USDon token address
   * @param _stablecoin       The stablecoin token address
   * @param _stablecoinOracle The stablecoin Chainlink price feed address
   * @param _maxOracleDataAge The maximum age of oracle data before being considered outdated
   */
  constructor(
    address _gmTokenManager,
    address _wallet,
    address _usdon,
    address _stablecoin,
    address _stablecoinOracle,
    uint256 _maxOracleDataAge
  ) {
    if (
      _gmTokenManager == address(0) ||
      _wallet == address(0) ||
      _usdon == address(0) ||
      _stablecoin == address(0) ||
      _stablecoinOracle == address(0)
    ) revert ZeroAddress();
    if (AggregatorV3Interface(_stablecoinOracle).decimals() != 8)
      revert InvalidOracleDecimals();
    if (_maxOracleDataAge == 0) revert InvalidMaxOracleDataAge();

    gmTokenManager = _gmTokenManager;
    wallet = _wallet;

    usdonNormalizer = 10 ** (IERC20Metadata(_usdon).decimals());
    stablecoinNormalizer = 10 ** (IERC20Metadata(_stablecoin).decimals());
    usdon = IERC20(_usdon);
    stablecoin = IERC20(_stablecoin);
    stablecoinOracle = AggregatorV3Interface(_stablecoinOracle);
    maxOracleDataAge = _maxOracleDataAge;
  }

  /**
   * @notice Swaps a stablecoin for USDon at a 1:1 rate (accounting for decimal differences)
   * @param  depositToken         The address of token to deposit (must match configured stablecoin)
   * @param  depositAmount        The amount of stablecoin to deposit (6 decimals)
   * @param  minimumUSDonReceived The minimum USDon to receive (18 decimals)
   * @return rwaAmountOut         The amount of USDon received (18 decimals)
   * @dev    This function has some effectively unused parameters to conform to the
   *         IUSDonManager interface. `depositToken` and `minimumUSDonReceived` are used
   *         purely for validation, but will be important in a multi-token implementation.
   */
  function subscribe(
    address depositToken,
    uint256 depositAmount,
    uint256 minimumUSDonReceived
  ) external override returns (uint256 rwaAmountOut) {
    if (msg.sender != gmTokenManager) revert OnlyGMTokenManager();
    if (depositToken != address(stablecoin)) revert InvalidDepositToken();
    _assertTokenMinimumStablecoinPrice();

    stablecoin.safeTransferFrom(gmTokenManager, wallet, depositAmount);
    rwaAmountOut = (depositAmount * usdonNormalizer) / stablecoinNormalizer;

    if (rwaAmountOut < minimumUSDonReceived) revert InsufficientUSDonReceived();
    usdon.safeTransferFrom(wallet, gmTokenManager, rwaAmountOut);
  }

  /**
   * @notice Swaps USDon for a stablecoin at a 1:1 rate (accounting for decimal differences)
   * @param  rwaAmount            The amount of USDon to redeem (18 decimals)
   * @param  receivingToken       The address of token to receive (must match configured stablecoin)
   * @param  minimumTokenReceived The minimum stablecoin to receive (6 decimals)
   * @return receiveTokenAmount   The amount of stablecoin received (6 decimals)
   * @dev    This function has some effectively unused parameters to conform to the
   *         IUSDonManager interface. `receivingToken` and `minimumTokenReceived` are used
   *         purely for validation, but will be important in a multi-token implementation.
   */
  function redeem(
    uint256 rwaAmount,
    address receivingToken,
    uint256 minimumTokenReceived
  ) external override returns (uint256 receiveTokenAmount) {
    if (msg.sender != gmTokenManager) revert OnlyGMTokenManager();
    if (receivingToken != address(stablecoin)) revert InvalidReceivingToken();
    _assertTokenMinimumStablecoinPrice();

    usdon.safeTransferFrom(gmTokenManager, wallet, rwaAmount);
    receiveTokenAmount = (rwaAmount * stablecoinNormalizer) / usdonNormalizer;

    if (receiveTokenAmount < minimumTokenReceived)
      revert InsufficientStablecoinReceived();
    stablecoin.safeTransferFrom(wallet, gmTokenManager, receiveTokenAmount);
  }

  /**
   * @notice Asserts that the stablecoin price from the Chainlink oracle is valid
   * @dev    Reverts if the oracle data is outdated or if the price is below the minimum
   *         in order to protect against stablecoin depegging events
   */
  function _assertTokenMinimumStablecoinPrice() internal view {
    (, int price, , uint256 updatedAt, ) = stablecoinOracle.latestRoundData();
    if (updatedAt < block.timestamp - maxOracleDataAge)
      revert OraclePriceOutdated();

    if (price < 0) revert StablecoinPriceBelowMinimum();
    if (uint256(price) < MINIMUM_STABLECOIN_PRICE)
      revert StablecoinPriceBelowMinimum();
  }
}