// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ITreasuryErrorsV2} from "./ITreasuryErrorsV2.sol";

address constant NATIVE_TOKEN = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;

/// @title ITreasuryV2
/// @notice Interface for the TreasuryV2 contract
interface ITreasuryV2 is ITreasuryErrorsV2 {
    /// @notice Emitted when the ICNT token address is set
    /// @param newICNToken The address of the new ICNT token
    event ICNTokenSet(IERC20 indexed newICNToken);

    /// @notice Emitted when the reserve contract address is set
    /// @param newReserveContract The address of the new reserve contract
    event ReserveContractSet(address indexed newReserveContract);

    /// @notice Emitted when a withdrawal to the reserve contract is made
    /// @param to The address of the recipient
    /// @param token The address of the token
    /// @param amount The amount of tokens to withdraw
    event WithdrawalToReserve(address indexed to, IERC20 indexed token, uint256 indexed amount);

    /// @notice Emitted when an owner withdrawal is made
    /// @param to The address of the recipient
    /// @param token The address of the token
    /// @param amount The amount of tokens to withdraw
    event OwnerWithdrawal(address indexed to, address indexed token, uint256 indexed amount);

    /// @notice Initializes the treasury v2
    /// @param governanceAddress The address of the governance account
    /// @param emergencyGovernanceAddress The address of the emergency governance account
    function initializeV2(address governanceAddress, address emergencyGovernanceAddress) external;

    /// @notice Sets the ICNT token address
    /// @param _icnToken The address of the ICNT token
    function setICNToken(IERC20 _icnToken) external;

    /// @notice Sets the reserve contract address
    /// @param _reserveContract The address of the reserve contract
    function setReserveContract(address _reserveContract) external;

    /// @notice Pauses the treasury
    function pause() external;

    /// @notice Unpauses the treasury
    function unpause() external;

    /// @notice Withdraws ICNT to the reserve contract
    /// @dev This function can only be called by the reserve contract, and can only transfer the specified amount of ICNT
    ///      to the reserve contract, as a security measure.
    /// @param amount The amount of ICNT to withdraw
    function withdrawICNTToReserve(uint256 amount) external;

    /// @notice Admin function to withdraw a specified token to a specified address
    /// @param tokenAddress The address of the token to withdraw
    /// @param amount The amount of tokens to withdraw
    /// @param to The address to send the tokens to
    function withdraw(address tokenAddress, uint256 amount, address to) external;

    /// @notice Returns the ICNT token address
    /// @return The address of the ICNT token
    function icnToken() external view returns (IERC20);

    /// @notice Returns the reserve contract address
    /// @return The address of the reserve contract
    function reserveContract() external view returns (address);
}
