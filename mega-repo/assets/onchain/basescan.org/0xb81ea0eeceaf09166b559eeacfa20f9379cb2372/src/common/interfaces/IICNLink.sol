// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {IERC721} from "@openzeppelin/contracts/token/ERC721/IERC721.sol";

/// @title IICNLink Interface
interface IICNLink is IERC721 {
    /// @notice Retrieves the activation time of the ICN Link
    /// @return uint256 The activation timestamp of the ICN Link
    function activationTime() external view returns (uint256);

    /// @notice Retrieves the duration time of the ICN Link
    /// @return uint256 The duration timestamp of the ICN Link
    function durationTime() external view returns (uint256);

    /// @notice Checks if the ICN Link is not activated
    /// @return bool True if the ICN Link is not activated, false otherwise
    function notActivated() external view returns (bool);

    /// @notice Retrieves the expiration time for a specific token.
    /// @param tokenId The ID of the token to get the expiration time for.
    /// @return uint256 The expiration timestamp of the token.
    function getExpirationTime(uint256 tokenId) external view returns (uint256);

    /// @notice Retrieves the duration time for a specific token.
    /// @param tokenId The ID of the token to get the duration time for.
    /// @return uint256 The duration timestamp of the token.
    function getDurationTime(uint256 tokenId) external view returns (uint256);
}
