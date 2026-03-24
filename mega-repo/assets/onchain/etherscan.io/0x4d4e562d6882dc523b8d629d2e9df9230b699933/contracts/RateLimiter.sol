// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import { Ownable } from "@openzeppelin/contracts/access/Ownable.sol";

import { IRateLimiter, RateLimitConfig, RateLimit } from "./interfaces/IRateLimiter.sol";

/**
 * @title RateLimiter
 * @notice This contract implements a rate limiter for outbound and inbound flows of tokens.
 * It allows the owner to configure rate limits for specific token IDs and destination endpoint IDs.
 * The contract also provides functions to check available amounts for sending and receiving tokens,
 * as well as to perform outflow and inflow operations while respecting the configured rate limits.
 */
contract RateLimiter is Ownable, IRateLimiter {
    // @dev Mappings for storing rate limits for outbound and inbound flows.
    mapping(bytes32 tokenId => mapping(uint32 eid => RateLimit)) public outboundLimits;
    mapping(bytes32 tokenId => mapping(uint32 eid => RateLimit)) public inboundLimits;

    // @dev The address of the Messenger contract, which is used to verify the caller in outflow and inflow functions.
    address public messenger;

    // @dev Modifier to control who can call inflow and outflow
    modifier onlyMessenger() {
        if (msg.sender != messenger) revert OnlyMessenger(msg.sender);
        _;
    }

    constructor(address _owner) Ownable(_owner) {}

    /**
     * @notice Sets the Messenger address, which is used to verify the caller in outflow and inflow functions.
     * @param _messenger The address of the Messenger contract.
     */
    function setMessenger(address _messenger) external onlyOwner {
        if (messenger == _messenger) revert MessengerIdempotent();
        messenger = _messenger;
        emit MessengerSet(_messenger);
    }

    /**
     * @notice Configures the rate limits for the specified tokenId and destination endpoint id.
     * @param _configs An array of `RateLimitConfig` structs representing the rate limit configurations.
     * - `remoteEid`: The destination endpoint id.
     * - `tokenId`: The identifier for the token.
     * - `outboundLimit`: This represents the maximum allowed amount within a given window for outflows.
     * - `outboundWindow`: Defines the duration of the rate limiting window for outflows.
     * - `inboundLimit`: This represents the maximum allowed amount within a given window for inflows.
     * - `inboundWindow`: Defines the duration of the rate limiting window for inflows.
     */
    function configureRateLimits(RateLimitConfig[] calldata _configs) external onlyOwner {
        for (uint256 i = 0; i < _configs.length; ++i) {
            RateLimitConfig memory cfg = _configs[i];
            // Configure outbound limit
            _configureRateLimit(outboundLimits[cfg.tokenId][cfg.remoteEid], cfg.outboundLimit, cfg.outboundWindow);
            // Configure inbound limit
            _configureRateLimit(inboundLimits[cfg.tokenId][cfg.remoteEid], cfg.inboundLimit, cfg.inboundWindow);
        }

        emit RateLimitsSet(_configs);
    }

    /**
     * @dev Configures a rate limit with new limit and window values while preserving decayed amount.
     * @param _rateLimit The rate limit to configure.
     * @param _newLimit The new limit value.
     * @param _newWindow The new window value.
     */
    function _configureRateLimit(RateLimit storage _rateLimit, uint256 _newLimit, uint256 _newWindow) internal {
        // Checkpoints the current amount by applying the previous rateLimit before we update it
        (, /*uint256 available*/ uint256 decayedAmount) = _getAmountAvailable(_rateLimit);

        // Update rate limit configuration
        _rateLimit.amount = decayedAmount;
        _rateLimit.limit = _newLimit;
        _rateLimit.window = _newWindow;
        _rateLimit.lastUpdated = block.timestamp;
    }

    /**
     * @notice Current amount that can be sent to this dst endpoint id for the given rate limit window and tokenId.
     * @param _tokenId The identifier for which the rate limit is being checked.
     * @dev _tokenAddress The address of the token from the corresponding Id.
     * @param _remoteEid The remote endpoint id.
     * @return sendable The current amount that can be sent.
     * @return currentOutbound The current amount used for outbound flows.
     * @return receivable The amount that can be received.
     * @return currentInbound The current amount used for inbound flows.
     */
    function getAmountsAvailable(
        bytes32 _tokenId,
        address /*_tokenAddress*/,
        uint32 _remoteEid
    ) external view returns (uint256 sendable, uint256 currentOutbound, uint256 receivable, uint256 currentInbound) {
        (sendable, currentOutbound) = _getAmountAvailable(outboundLimits[_tokenId][_remoteEid]);
        (receivable, currentInbound) = _getAmountAvailable(inboundLimits[_tokenId][_remoteEid]);
    }

    /**
     * @dev Gets the available amount and decayed amount used for a given rate limit after applying decay.
     * @param _rateLimit The rate limit to check.
     * @return available The available amount that can be used within the rate limit.
     * @return decayedAmount The current amount after applying decay.
     */
    function _getAmountAvailable(
        RateLimit storage _rateLimit
    ) internal view returns (uint256 available, uint256 decayedAmount) {
        decayedAmount = _calculateDecay(_rateLimit.amount, _rateLimit.lastUpdated, _rateLimit.limit, _rateLimit.window);
        available = _rateLimit.limit > decayedAmount ? _rateLimit.limit - decayedAmount : 0;
    }

    /**
     * @notice Verifies whether the specified amount falls within the rate limit constraints for the targeted
     * endpoint ID. On successful verification, it updates amountUsed and lastUpdated. If the amount exceeds
     * the rate limit, the operation reverts.
     * @param _tokenId The identifier for which the rate limit is being checked.
     * @dev _tokenAddress The address of the token from the corresponding Id.
     * @param _dstEid The destination endpoint id.
     * @param _amount The amount to outflow.
     */
    function outflow(
        bytes32 _tokenId,
        address /*_tokenAddress*/,
        uint32 _dstEid,
        uint256 _amount
    ) external onlyMessenger {
        _updateRateLimits(outboundLimits[_tokenId][_dstEid], inboundLimits[_tokenId][_dstEid], _amount);
    }

    /**
     * @notice To be used when you want to calculate your rate limits as a function of net outbound AND inbound.
     * @param _tokenId The identifier for which the rate limit is being checked.
     * @dev _tokenAddress The address of the token from the corresponding Id.
     * @param _srcEid The source endpoint id.
     * @param _amount The amount to inflow.
     */
    function inflow(
        bytes32 _tokenId,
        address /*_tokenAddress*/,
        uint32 _srcEid,
        uint256 _amount
    ) external onlyMessenger {
        _updateRateLimits(inboundLimits[_tokenId][_srcEid], outboundLimits[_tokenId][_srcEid], _amount);
    }

    /**
     * @dev Updates both primary and secondary rate limits for a flow operation.
     * @param _limitA The primary rate limit to update (outbound for outflow, inbound for inflow).
     * @param _limitB The secondary rate limit to update (inbound for outflow, outbound for inflow).
     * @param _amount The amount of the flow operation.
     */
    function _updateRateLimits(RateLimit storage _limitA, RateLimit storage _limitB, uint256 _amount) internal {
        // 1) Process primary limit - check availability and update
        (uint256 availableAmountA, uint256 decayedAmountA) = _getAmountAvailable(_limitA);
        if (_amount > availableAmountA) revert RateLimitExceeded();
        _limitA.amount = decayedAmountA + _amount;
        _limitA.lastUpdated = block.timestamp;

        // 2) Process secondary limit - update with subtraction
        (, /*uint256 availableAmountB*/ uint256 decayedAmountB) = _getAmountAvailable(_limitB);
        _limitB.amount = decayedAmountB > _amount ? decayedAmountB - _amount : 0;
        _limitB.lastUpdated = block.timestamp;
    }

    /**
     * @dev Calculates the decay of the amount based on the time elapsed since the last update.
     * @param _amount The current amount tracked against the rate limit.
     * @param _lastUpdated The timestamp of the last update.
     * @param _limit The maximum allowed amount within a given window.
     * @param _window The duration of the rate limiting window.
     * @return decayedAmount The decayed amount after applying the decay based on elapsed time.
     */
    function _calculateDecay(
        uint256 _amount,
        uint256 _lastUpdated,
        uint256 _limit,
        uint256 _window
    ) internal view returns (uint256 decayedAmount) {
        uint256 elapsed = block.timestamp - _lastUpdated;
        // @dev if window is set to 0, then the full decay is basically immediate
        uint256 decay = (_limit * elapsed) / (_window > 0 ? _window : 1);
        decayedAmount = _amount > decay ? _amount - decay : 0;
    }
}
