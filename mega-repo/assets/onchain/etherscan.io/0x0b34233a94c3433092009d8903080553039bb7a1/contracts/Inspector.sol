// SPDX-License-Identifier: MIT
pragma solidity 0.8.22;

import { Ownable } from "@openzeppelin/contracts/access/Ownable.sol";

import { IInspector } from "./interfaces/IInspector.sol";

/**
 * @title Inspector
 * @notice Handles inspection of messages before they are sent on the src chain.
 * @dev The owner will be the same owner of the Messenger, and OFT etc. We will route all calls via that owner.
 */
contract Inspector is IInspector, Ownable {
    // @dev Paused id mapping, where the key is the id and the value is a boolean indicating if it is paused.
    mapping(bytes32 id => bool paused) public pausedIds;

    // @dev Global paused state for the inspector, which can be used to pause all operations.
    bool public globalPause;

    constructor(address _owner) Ownable(_owner) {}

    /**
     * @notice Sets the global paused value.
     * @param _paused The state of the global pause.
     * @dev Sets a global pause state applied to all messages that are inspected.
     */
    function setGlobalPaused(bool _paused) external onlyOwner {
        // @dev If pause is already set to expected, revert
        if (globalPause == _paused) revert GlobalPausedIdempotent(_paused);

        globalPause = _paused;
        emit GlobalPausedSet(_paused);
    }

    /**
     * @notice Sets the id paused value.
     * @param _id The identifier.
     * @param _paused The state of the pause.
     * @dev Sets the pause state for a given 'id'.
     */
    function setIdPaused(bytes32 _id, bool _paused) external onlyOwner {
        // @dev If id pause is already set to expected, revert
        if (pausedIds[_id] == _paused) revert IdPausedIdempotent(_id, _paused);

        pausedIds[_id] = _paused;
        emit IdPausedSet(_id, _paused);
    }

    /**
     * @notice Allows the inspectee to examine LayerZero message contents and optionally throw a revert if invalid.
     * @param _id The identifier being inspected.
     * @dev _message The message payload to be inspected, currently unused.
     * @dev _options Additional options or parameters for inspection, currently unused.
     */
    function inspect(bytes32 _id, bytes calldata /*_message*/, bytes calldata /*_options*/) external view {
        if (globalPause) revert GlobalPaused();
        if (pausedIds[_id]) revert IdPaused(_id);
    }
}
