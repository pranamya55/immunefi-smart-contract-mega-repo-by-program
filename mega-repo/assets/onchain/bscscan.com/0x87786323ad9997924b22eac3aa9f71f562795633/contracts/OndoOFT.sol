// SPDX-License-Identifier: MIT
pragma solidity 0.8.22;

import { IERC20Metadata } from "@openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol";
import { Ownable } from "@openzeppelin/contracts/access/Ownable.sol";

import { ILayerZeroEndpointV2 } from "@layerzerolabs/oapp-evm/contracts/oapp/interfaces/IOAppCore.sol";
import { Origin } from "@layerzerolabs/oapp-evm/contracts/oapp/OApp.sol";

import { OFTMsgCodec } from "@layerzerolabs/oft-evm/contracts/libs/OFTMsgCodec.sol";
import { OFTComposeMsgCodec } from "@layerzerolabs/oft-evm/contracts/libs/OFTComposeMsgCodec.sol";
import { IMintBurnVoidReturn } from "./interfaces/IMintBurnVoidReturn.sol";

import { IMessenger, MessagingParam } from "./interfaces/IMessenger.sol";

import { IOndoOFT, SendParam, MessagingFee, MessagingReceipt, OFTLimit, OFTFeeDetail, OFTReceipt } from "./interfaces/IOndoOFT.sol";

import { DecimalConversions } from "./libs/DecimalConversions.sol";

contract OndoOFT is IOndoOFT, Ownable {
    using DecimalConversions for uint256;
    using DecimalConversions for uint64;
    using OFTMsgCodec for bytes;
    using OFTMsgCodec for bytes32;

    IMessenger internal messenger;
    ILayerZeroEndpointV2 public immutable endpoint;
    IMintBurnVoidReturn internal immutable innerToken;
    bytes32 public immutable tokenId;

    constructor(address _messenger, address _token, bytes32 _tokenId, address _owner) Ownable(_owner) {
        messenger = IMessenger(_messenger);
        endpoint = messenger.endpoint();
        innerToken = IMintBurnVoidReturn(_token);
        tokenId = _tokenId;

        // @dev Sanity check that the underlying token is 18 decimals, to ensure conversions are correct.
        if (IERC20Metadata(_token).decimals() != DecimalConversions.LOCAL_DECIMALS) {
            revert InvalidLocalDecimals();
        }
    }

    /**
     * @notice Sets the messenger address for the OFT contract.
     * @param _messenger The address of the messenger contract.
     *
     * @dev This function can only be called by the owner of the contract.
     * It allows changing the messenger address to a new one.
     */
    function setMessenger(address _messenger) external onlyOwner {
        IMessenger newMessenger = IMessenger(_messenger);

        // @dev Check that the new messenger has the same endpoint as the current messenger.
        if (address(newMessenger.endpoint()) != address(endpoint)) {
            revert EndpointMismatch(address(newMessenger.endpoint()), address(endpoint));
        }

        messenger = newMessenger;
        emit MessengerSet(_messenger);
    }

    /**
     * @notice Retrieves the address of the underlying ERC20 implementation.
     * @return The address of the adapted ERC-20 token.
     *
     * @dev In the case of OndoOFT, address(this) and erc20 are NOT the same contract.
     */
    function token() public view returns (address) {
        return address(innerToken);
    }

    /**
     * @notice Indicates whether the OFT contract requires approval of the 'token()' to send.
     * @return requiresApproval Needs approval of the underlying token implementation.
     *
     * @dev In the case of this OFT, approval is NOT required. Because this OFT has mint/burn privileges.
     */
    function approvalRequired() external pure virtual returns (bool) {
        return false;
    }

    /**
     * @notice Retrieves interfaceID and the version of the OFT.
     * @return interfaceId The interface ID.
     * @return version The version.
     *
     * @dev interfaceId: This specific interface ID is '0xa42519c0'.
     * @dev version: Indicates a cross-chain compatible msg encoding with other OFTs.
     * @dev If a new feature is added to the OFT cross-chain msg encoding, the version will be incremented.
     * ie. localOFT version(x,1) CAN send messages to remoteOFT version(x,1)
     */
    function oftVersion() external pure virtual returns (bytes4 interfaceId, uint64 version) {
        // @dev The nature of this OFT is very different, we are using a shared single OApp to handle the oftMessaging
        // between multiple ofts on a given chain. This means we have a slightly different encoding. Further we
        // also don't have a typical lzReceive() on this contract.
        return (type(IOndoOFT).interfaceId, 1);
    }

    /**
     * @notice Retrieves the shared decimals of the OFT.
     * @return The shared decimals of the OFT.
     *
     * @dev Sets an implicit cap on the amount of tokens,
     * over uint64.max() will need some sort of outbound cap / totalSupply cap.
     * Lowest common decimal denominator between chains.
     * Defaults to 6 decimal places to provide up to 18,446,744,073,709.551615 units (max uint64).
     * ie. 4 sharedDecimals would be 1,844,674,407,370,955.1615
     */
    function sharedDecimals() public view virtual returns (uint8) {
        return DecimalConversions.SHARED_DECIMALS;
    }

    /**
     * @notice Provides the fee breakdown and settings data for an OFT. Unused in the default implementation.
     * @param _sendParam The parameters for the send operation.
     * @return oftLimit The OFT limit information.
     * @return oftFeeDetails The details of OFT fees.
     * @return oftReceipt The OFT receipt information.
     */
    function quoteOFT(
        SendParam calldata _sendParam
    )
        external
        view
        virtual
        returns (OFTLimit memory oftLimit, OFTFeeDetail[] memory oftFeeDetails, OFTReceipt memory oftReceipt)
    {
        uint256 minAmountLD = 0; // Unused in the default implementation.

        // @dev Pulls the current rateLimit maximum amount available,
        // by calling the messenger who routes to the rateLimiter.
        (
            uint256 sendable /*uint256 currentOutbound*/ /*uint256 receivable*/ /*uint256 currentInbound*/,
            ,
            ,

        ) = messenger.getRateLimitedAmounts(tokenId, address(innerToken), _sendParam.dstEid);
        uint256 maxAmountLD = sendable;

        oftLimit = OFTLimit(minAmountLD, maxAmountLD);

        // Unused in the default implementation; reserved for future complex fee details.
        oftFeeDetails = new OFTFeeDetail[](0);

        // @dev This is the same as the send() operation, but without the actual send.
        // - amountSentLD is the amount in local decimals that would be sent from the sender.
        // - amountReceivedLD is the amount in local decimals that will be credited to the recipient on the remote OFT.
        // @dev The amountSentLD MIGHT not equal the amount the user actually receives. HOWEVER, the default does.
        (uint256 amountSentLD, uint256 amountReceivedLD) = _debitView(
            _sendParam.amountLD,
            _sendParam.minAmountLD,
            _sendParam.dstEid
        );
        oftReceipt = OFTReceipt(amountSentLD, amountReceivedLD);
    }

    /**
     * @notice Provides a quote for the send() operation.
     * @param _sendParam The parameters for the send() operation.
     * @param _payInLzToken Flag indicating whether the caller is paying in the LZ token.
     * @return msgFee The calculated LayerZero messaging fee from the send() operation.
     *
     * @dev MessagingFee: LayerZero msg fee
     *  - nativeFee: The native fee.
     *  - lzTokenFee: The lzToken fee.
     */
    function quoteSend(
        SendParam calldata _sendParam,
        bool _payInLzToken
    ) external view virtual returns (MessagingFee memory msgFee) {
        // @dev Mock the amount to receive, this is the same operation used in the send().
        // The quote is as similar as possible to the actual send() operation.
        (, uint256 amountReceivedLD) = _debitView(_sendParam.amountLD, _sendParam.minAmountLD, _sendParam.dstEid);

        // @dev Calculates the LayerZero fee for the send() operation.
        return
            messenger.quoteSend(
                MessagingParam({
                    dstEid: _sendParam.dstEid,
                    to: _sendParam.to,
                    amountLD: amountReceivedLD,
                    extraOptions: _sendParam.extraOptions,
                    composeMsg: _sendParam.composeMsg
                }),
                _payInLzToken
            );
    }

    /**
     * @notice Executes the send operation.
     * @param _sendParam The parameters for the send operation.
     * @param _fee The calculated fee for the send() operation.
     *      - nativeFee: The native fee.
     *      - lzTokenFee: The lzToken fee.
     * @param _refundAddress The address to receive any excess funds.
     * @return msgReceipt The receipt for the send operation.
     * @return oftReceipt The OFT receipt information.
     *
     * @dev MessagingReceipt: LayerZero msg receipt
     *  - guid: The unique identifier for the sent message.
     *  - nonce: The nonce of the sent message.
     *  - fee: The LayerZero fee incurred for the message.
     */
    function send(
        SendParam calldata _sendParam,
        MessagingFee calldata _fee,
        address _refundAddress
    ) external payable returns (MessagingReceipt memory msgReceipt, OFTReceipt memory oftReceipt) {
        // @dev Applies the token transfers regarding this send() operation.
        // - amountSentLD is the amount in local decimals that was ACTUALLY sent/debited from the sender.
        // - amountReceivedLD is the amount in local decimals that will be received/credited to the recipient.
        (uint256 amountSentLD, uint256 amountReceivedLD) = _debit(
            msg.sender,
            _sendParam.amountLD,
            _sendParam.minAmountLD,
            _sendParam.dstEid
        );

        // @dev Sends the message to the LayerZero endpoint and returns the LayerZero msg receipt.
        msgReceipt = messenger.send{ value: msg.value }(
            MessagingParam({
                dstEid: _sendParam.dstEid,
                to: _sendParam.to,
                amountLD: amountReceivedLD,
                extraOptions: _sendParam.extraOptions,
                composeMsg: _sendParam.composeMsg
            }),
            _fee,
            _refundAddress
        );
        // @dev Formulate the OFT receipt.
        oftReceipt = OFTReceipt(amountSentLD, amountReceivedLD);

        emit OFTSent(msgReceipt.guid, _sendParam.dstEid, msg.sender, amountSentLD, amountReceivedLD);
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
     *
     * @dev This varies from the traditional lzReceive() because the OFT itself is NOT an OApp,
     * and thus we need to validate it comes from the current Messenger contract
     */
    function messagingReceive(
        Origin calldata _origin,
        bytes32 _guid,
        bytes calldata _message,
        address /*_executor*/,
        bytes calldata /*_extraData*/
    ) external {
        if (msg.sender != address(messenger)) revert OnlyMessenger(msg.sender);

        // @dev The src sending chain doesn't know the address length on this chain (potentially non-evm)
        // Thus everything is bytes32() encoded in flight.
        address toAddress = _message.sendTo().bytes32ToAddress();
        // @dev Credit the amountLD to the recipient and return the ACTUAL amount received in local decimals
        uint256 amountReceivedLD = _credit(toAddress, _message.amountSD().toLD(), _origin.srcEid);

        if (_message.isComposed()) {
            // @dev Proprietary composeMsg format for the OFT.
            bytes memory composeMsg = OFTComposeMsgCodec.encode(
                _origin.nonce,
                _origin.srcEid,
                amountReceivedLD,
                _message.composeMsg()
            );

            // @dev Stores the lzCompose payload that will be executed in a separate tx.
            // Standardizes functionality for executing arbitrary contract invocation on some non-evm chains.
            // @dev The off-chain executor will process the msg based on the src-chain-caller's compose options passed.
            // @dev The index is used when an OApp needs to compose multiple msgs on lzReceive.
            // For default OFT implementation there is only 1 compose msg per lzReceive, thus it's always 0.
            endpoint.sendCompose(toAddress, _guid, 0 /* the index of the composed message*/, composeMsg);
        }

        emit OFTReceived(_guid, _origin.srcEid, toAddress, amountReceivedLD);
    }

    /**
     * @notice Internal function to mock the amount mutation from a OFT debit() operation.
     * @param _amountLD The amount to send in local decimals.
     * @param _minAmountLD The minimum amount to send in local decimals.
     * @dev _dstEid The destination endpoint ID.
     * @return amountSentLD The amount sent, in local decimals.
     * @return amountReceivedLD The amount to be received on the remote chain, in local decimals.
     */
    function _debitView(
        uint256 _amountLD,
        uint256 _minAmountLD,
        uint32 /*_dstEid*/
    ) internal view virtual returns (uint256 amountSentLD, uint256 amountReceivedLD) {
        // @dev Remove the dust so nothing is lost on the conversion between chains with different decimals.
        amountSentLD = _amountLD.removeDust();
        // @dev The amount to send is the same as amount received in the default implementation.
        amountReceivedLD = amountSentLD;

        // @dev Check for slippage.
        if (amountReceivedLD < _minAmountLD) {
            revert SlippageExceeded(amountReceivedLD, _minAmountLD);
        }
    }

    /**
     * @notice Burns tokens from the sender's specified balance.
     * @param _from The address to debit the tokens from.
     * @param _amountLD The amount of tokens to send in local decimals.
     * @param _minAmountLD The minimum amount to send in local decimals.
     * @param _dstEid The destination chain ID.
     * @return amountSentLD The amount sent in local decimals.
     * @return amountReceivedLD The amount received in local decimals on the remote.
     */
    function _debit(
        address _from,
        uint256 _amountLD,
        uint256 _minAmountLD,
        uint32 _dstEid
    ) internal returns (uint256 amountSentLD, uint256 amountReceivedLD) {
        (amountSentLD, amountReceivedLD) = _debitView(_amountLD, _minAmountLD, _dstEid);
        // Burns tokens from the caller.
        innerToken.burnFrom(_from, amountSentLD);
    }

    /**
     * @notice Credits tokens to the specified address.
     * @param _to The address to credit the tokens to.
     * @param _amountLD The amount of tokens to credit in local decimals.
     * @dev _srcEid The source chain ID.
     * @return amountReceivedLD The amount of tokens ACTUALLY received in local decimals.
     */
    function _credit(address _to, uint256 _amountLD, uint32 /* _srcEid */) internal returns (uint256 amountReceivedLD) {
        if (_to == address(0x0)) _to = address(0xdead); // _mint(...) does not support address(0x0)
        // Mints the tokens and transfers to the recipient.
        innerToken.mint(_to, _amountLD);
        // In the case of NON-default OFTAdapter, the amountLD MIGHT not be equal to amountReceivedLD.
        return _amountLD;
    }
}
