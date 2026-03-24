// SPDX-License-Identifier: MIT
pragma solidity 0.8.22;

import { Ownable } from "@openzeppelin/contracts/access/Ownable.sol";

import { OApp, Origin } from "@layerzerolabs/oapp-evm/contracts/oapp/OApp.sol";
import { OAppOptionsType3 } from "@layerzerolabs/oapp-evm/contracts/oapp/libs/OAppOptionsType3.sol";
import { OFTMsgCodec } from "@layerzerolabs/oft-evm/contracts/libs/OFTMsgCodec.sol";

import { IInspector } from "./interfaces/IInspector.sol";
import { IMessenger, MessagingParam } from "./interfaces/IMessenger.sol";
import { IOndoOFT, MessagingFee, MessagingReceipt } from "./interfaces/IOndoOFT.sol";
import { OndoOFT } from "./OndoOFT.sol";

import { DecimalConversions } from "./libs/DecimalConversions.sol";
import { IRateLimiter } from "./interfaces/IRateLimiter.sol";

/**
 * @title Messenger
 * @notice The Messenger contract is an OApp that routes OFT messages across chains.
 * It handles the registration of OFT contracts, message sending, and rate limiting.
 */
contract Messenger is IMessenger, OApp, OAppOptionsType3 {
    using DecimalConversions for uint256;

    // @dev Mappings to track the registered OFT contracts by their tokenId and vice versa.
    mapping(bytes32 tokenId => address oftAddress) public idToOft;
    mapping(bytes32 tokenId => address tokenAddress) public idToToken;
    mapping(address oftAddress => bytes32 tokenId) public oftToId;

    // @dev Msg types used for indexing into enforced options etc.
    uint16 public constant SEND = 1;
    uint16 public constant SEND_AND_CALL = 2;

    // @dev Address of an optional contract to inspect both 'message' and 'options' based on 'tokenId'.
    IInspector public inspector;
    // @dev Address of the rateLimiter, which validates against inflows and outflows of tokens.
    IRateLimiter public rateLimiter;

    constructor(
        address _inspector,
        address _rateLimiter,
        address _endpoint,
        address _delegate
    ) OApp(_endpoint, _delegate) Ownable(_delegate) {
        _setInspector(_inspector);
        _setRateLimiter(_rateLimiter);
    }

    /**
     * @notice Sets the inspector address, which is used to inspect messages before they are sent.
     * @param _inspector The address of the inspector contract.
     * @dev This can be set to address(0) if no inspector is required.
     */
    function setInspector(address _inspector) public virtual onlyOwner {
        _setInspector(_inspector);
    }

    // @dev Internal function to set the inspector address.
    function _setInspector(address _inspector) internal {
        // @dev This can be set to address(0) if no inspector is required.
        inspector = IInspector(_inspector);
        emit InspectorSet(_inspector);
    }

    /**
     * @notice Sets the rate limiter address, which is used to validate inflows and outflows of tokens.
     * @param _rateLimiter The address of the rate limiter contract.
     */
    function setRateLimiter(address _rateLimiter) external onlyOwner {
        _setRateLimiter(_rateLimiter);
    }

    // @dev Internal function to set the rate limiter address.
    function _setRateLimiter(address _rateLimiter) internal {
        if (_rateLimiter == address(0)) revert InvalidRateLimiter();
        rateLimiter = IRateLimiter(_rateLimiter);
        emit RateLimiterSet(_rateLimiter);
    }

    /**
     * @notice Registers a new token with its corresponding generated OFT contract.
     * @param _tokenId The unique identifier for the token.
     * @param _tokenAddress The address of the token contract.
     * @return oftAddress The address of the newly created OndoOFT contract.
     *
     * @dev This function is more limited in that it can only register a brand new tokenId, it cannot alter existing.
     */
    function registerToken(bytes32 _tokenId, address _tokenAddress) external onlyOwner returns (address oftAddress) {
        if (_tokenId == bytes32(0) || _tokenAddress == address(0)) {
            // @dev Cannot register with invalid token details.
            revert InvalidTokenRegistration(_tokenId, _tokenAddress);
        }

        if (idToOft[_tokenId] != address(0) || idToToken[_tokenId] != address(0)) {
            // @dev If the tokenId is already registered, we should revert.
            revert TokenAlreadyRegistered(_tokenId, _tokenAddress);
        }

        // @dev Create a new OndoOFT contract for the given tokenId and tokenAddress.
        oftAddress = address(new OndoOFT(address(this), _tokenAddress, _tokenId, owner()));

        idToOft[_tokenId] = oftAddress;
        idToToken[_tokenId] = _tokenAddress;
        oftToId[oftAddress] = _tokenId;

        emit TokenRegistered(_tokenId, _tokenAddress, oftAddress);
    }

    /**
     * @notice Deregisters an existing token and clears all associated mappings.
     * @param _tokenId The unique identifier for the token to be deregistered.
     *
     * @dev This function completely removes the token from all mappings, making it no longer usable.
     */
    function deregisterToken(bytes32 _tokenId) external onlyOwner {
        // @dev Validate that the token is currently registered.
        address oftAddress = idToOft[_tokenId];
        address tokenAddress = idToToken[_tokenId];
        if (oftAddress == address(0) || tokenAddress == address(0)) {
            revert TokenNotRegistered(_tokenId);
        }

        // @dev Clear all mappings, this prevents orphaned state.
        delete idToOft[_tokenId];
        delete idToToken[_tokenId];
        delete oftToId[oftAddress];

        emit TokenDeregistered(_tokenId, tokenAddress, oftAddress);
    }

    /**
     * @notice Registers a token with an existing OFT contract address.
     * @param _tokenId The unique identifier for the token.
     * @param _tokenAddress The address of the token contract.
     * @param _oftAddress The address of the existing OFT contract.
     *
     * @dev This function allows registering with a pre-existing OFT contract instead of creating a new one.
     * @dev Useful for fixing registration mistakes or migrating to new OFT contracts.
     */
    function registerTokenWithOFT(bytes32 _tokenId, address _tokenAddress, address _oftAddress) external onlyOwner {
        // @dev Input validation - check for zero values, matching tokenId and token address
        if (
            _tokenId == bytes32(0) ||
            _tokenAddress == address(0) ||
            _oftAddress == address(0) ||
            IOndoOFT(_oftAddress).tokenId() != _tokenId ||
            IOndoOFT(_oftAddress).token() != _tokenAddress
        ) {
            revert InvalidTokenRegistrationWithOFT(_tokenId, _tokenAddress, _oftAddress);
        }

        // @dev Ensure the tokenId is not already registered.
        if (idToOft[_tokenId] != address(0) || idToToken[_tokenId] != address(0)) {
            revert TokenAlreadyRegistered(_tokenId, _tokenAddress);
        }

        // @dev Ensure the OFT address is not already registered to another token.
        if (oftToId[_oftAddress] != bytes32(0)) {
            revert OFTAlreadyRegistered(_oftAddress, oftToId[_oftAddress]);
        }

        // @dev Set all mappings.
        idToOft[_tokenId] = _oftAddress;
        idToToken[_tokenId] = _tokenAddress;
        oftToId[_oftAddress] = _tokenId;

        emit TokenRegistered(_tokenId, _tokenAddress, _oftAddress);
    }

    /**
     * @notice Provides rate limit available for sending and receiving tokens by routing the call to the rateLimiter.
     * @param _tokenId The identifier for which the rate limit is being checked.
     * @param _tokenAddress The address of the token from the corresponding Id.
     * @param _remoteEid The remote endpoint id.
     * @return sendable The current amount that can be sent.
     * @return currentOutbound The current amount used for outbound flows.
     * @return receivable The amount that can be received.
     * @return currentInbound The current amount used for inbound flows.
     */
    function getRateLimitedAmounts(
        bytes32 _tokenId,
        address _tokenAddress,
        uint32 _remoteEid
    ) external view returns (uint256 sendable, uint256 currentOutbound, uint256 receivable, uint256 currentInbound) {
        (sendable, currentOutbound, receivable, currentInbound) = rateLimiter.getAmountsAvailable(
            _tokenId,
            _tokenAddress,
            _remoteEid
        );
    }

    /**
     * @notice Provides a quote for the send() operation.
     * @param _messagingParam The parameters for the send() operation.
     * @param _payInLzToken Flag indicating whether the caller is paying in the LZ token.
     * @return msgFee The calculated LayerZero messaging fee from the send() operation.
     *
     * @dev MessagingFee: LayerZero msg fee
     *  - nativeFee: The native fee.
     *  - lzTokenFee: The lzToken fee.
     */
    function quoteSend(
        MessagingParam calldata _messagingParam,
        bool _payInLzToken
    ) external view virtual returns (MessagingFee memory msgFee) {
        // @dev Quote should be called via the OFT, not directly here
        bytes32 tokenId = oftToId[msg.sender];
        address tokenAddress = idToToken[tokenId];
        if (tokenId == bytes32(0) || tokenAddress == address(0)) revert InvalidOFT(msg.sender);

        // @dev Builds the options and OFT message to quote in the endpoint.
        (bytes memory message, bytes memory options) = _buildMsgAndOptions(tokenId, _messagingParam);

        (
            uint256 sendable /*uint256 currentOutbound*/ /*uint256 receivable*/ /*uint256 currentInbound*/,
            ,
            ,

        ) = rateLimiter.getAmountsAvailable(tokenId, tokenAddress, _messagingParam.dstEid);
        if (_messagingParam.amountLD > sendable) revert IRateLimiter.RateLimitExceeded();

        // @dev Calculates the LayerZero fee for the send() operation.
        return _quote(_messagingParam.dstEid, message, options, _payInLzToken);
    }

    /**
     * @notice Executes and routes the send function through the endpoint.
     * @param _messagingParam The parameters for the send() operation.
     * @param _fee The calculated fee for the send() operation.
     *      - nativeFee: The native fee.
     *      - lzTokenFee: The lzToken fee.
     * @param _refundAddress The address to receive any excess funds.
     * @return msgReceipt The receipt for the send operation.
     *
     * @dev Since this is an external version, MUST index on the msg.sender to verify it's a valid OFT calling this.
     *
     * @dev MessagingReceipt: LayerZero msg receipt
     *  - guid: The unique identifier for the sent message.
     *  - nonce: The nonce of the sent message.
     *  - fee: The LayerZero fee incurred for the message.
     */
    function send(
        MessagingParam calldata _messagingParam,
        MessagingFee calldata _fee,
        address _refundAddress
    ) public payable returns (MessagingReceipt memory msgReceipt) {
        // @dev Verify this is a valid oft calling this contract.
        bytes32 tokenId = oftToId[msg.sender];
        address tokenAddress = idToToken[tokenId];
        if (tokenId == bytes32(0) || tokenAddress == address(0)) revert InvalidOFT(msg.sender);

        // @dev Builds the options and OFT message to quote in the endpoint.
        (bytes memory message, bytes memory options) = _buildMsgAndOptions(tokenId, _messagingParam);

        // @dev Checkpoint the rate limit outflow
        rateLimiter.outflow(tokenId, tokenAddress, _messagingParam.dstEid, _messagingParam.amountLD);

        // @dev Sends the message to the LayerZero endpoint and returns the LayerZero msg receipt.
        msgReceipt = _lzSend(_messagingParam.dstEid, message, options, _fee, _refundAddress);
    }

    /**
     * @notice Internal function to build the message and options.
     * @param _tokenId The token identifier.
     * @param _messagingParam The parameters for the send() operation.
     * @return message The encoded message.
     * @return options The encoded options.
     */
    function _buildMsgAndOptions(
        bytes32 _tokenId,
        MessagingParam calldata _messagingParam
    ) internal view returns (bytes memory message, bytes memory options) {
        bool hasCompose;
        // @dev Generated message has the msg.sender encoded into the payload so the remote knows who the caller is.
        (message, hasCompose) = OFTMsgCodec.encode(
            _messagingParam.to,
            // @dev Convert local decimals to shared decimals, dust loss should be handled in the OFT contract
            _messagingParam.amountLD.toSD(),
            // @dev Must include a non-empty bytes if you want to compose, EVEN if you don't need it on the remote.
            // EVEN if you don't require an arbitrary payload to be sent... eg. '0x01'
            _messagingParam.composeMsg
        );

        // @dev Need to append the tokenId to the message so the remote can identify which token this is.
        message = abi.encodePacked(_tokenId, message);

        // @dev Combine the caller's _extraOptions with the enforced options via the OAppOptionsType3.
        options = combineOptions(
            _messagingParam.dstEid,
            hasCompose ? SEND_AND_CALL : SEND, // @dev Change the msg type depending if it's composed or not.
            _messagingParam.extraOptions
        );

        // @dev Optionally inspect the message and options depending if the OApp owner has set a msg inspector.
        if (address(inspector) != address(0)) inspector.inspect(_tokenId, message, options);
    }

    /**
     * @notice Internal function to handle the receive on the LayerZero endpoint.
     * @param _origin The origin information.
     *  - srcEid: The source chain endpoint ID.
     *  - sender: The sender address from the src chain.
     *  - nonce: The nonce of the LayerZero message.
     * @param _guid The unique identifier for the received LayerZero message.
     * @param _message The encoded message.
     * @dev _executor The address of the executor.
     * @dev _extraData Additional data.
     */
    function _lzReceive(
        Origin calldata _origin,
        bytes32 _guid,
        bytes calldata _message,
        address _executor,
        bytes calldata _extraData
    ) internal override {
        // @dev Extract the tokenId which is the first 32 bytes of the Messenger.msg
        bytes32 tokenId = bytes32(_message[:32]);

        // If token id is not registered, need to revert until it is supported.
        // In the event this fails, transaction will need to be retried AFTER the tokenId is registered
        address oftAddress = idToOft[tokenId];
        address tokenAddress = idToToken[tokenId];
        if (oftAddress == address(0) || tokenAddress == address(0)) revert InvalidTokenId(tokenId);

        // @dev Checkpoint the rate limit inflow, and parse out the amountLD
        rateLimiter.inflow(
            tokenId,
            tokenAddress,
            _origin.srcEid,
            DecimalConversions.toLD(OFTMsgCodec.amountSD(_message[32:]))
        );

        // Forward to the correct OFT contract
        IOndoOFT(oftAddress).messagingReceive(_origin, _guid, _message[32:], _executor, _extraData);
    }
}
