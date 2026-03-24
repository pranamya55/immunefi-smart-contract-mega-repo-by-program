// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

import {IReservePoolErrorsV2} from "./IReservePoolErrorsV2.sol";

/// @title IReservePoolV2
/// @notice Interface for the ReservePoolV2 contract
interface IReservePoolV2 is IReservePoolErrorsV2 {
    event ICNTokenSet(IERC20 indexed newICNToken);
    event ProtocolContractSet(address indexed newProtocolContract);

    // Event emitted when an account is whitelisted
    event AccountWhitelisted(address indexed account);

    // Event emitted when an account is unwhitelisted
    event AccountUnwhitelisted(address indexed account);

    // Event emitted when tokens are deposited in the reserve pool to reward a region
    event DepositedRegionBaseReward(string indexed regionId, uint256 indexed baseReward);

    event DepositedAmountFromWhitelistedAccount(address indexed account, uint256 indexed depositAmount);

    // Event emitted when tokens are withdrawn from the reserve pool to reward a region
    event WithdrawnRegionBaseReward(string indexed regionId, uint256 indexed amount);

    // Event emitted when tokens are withdrawn from the reserve pool
    event OwnerWithdrawal(address indexed to, uint256 indexed amount);

    /// @notice Initializes the reserve pool v2
    /// @param governanceAddress The address of the governance account
    /// @param emergencyGovernanceAddress The address of the emergency governance account
    function initializeV2(address governanceAddress, address emergencyGovernanceAddress) external;

    /// @notice Sets the protocol contract address
    /// @param _protocolContract The address of the protocol contract
    function setProtocolContract(address _protocolContract) external;

    /// @notice Sets the ICNT token address
    /// @param _icnToken The address of the ICNT token
    function setICNToken(IERC20 _icnToken) external;

    /// @notice Allow an account to deposit tokens for rewarding
    /// @param account The address of the account to whitelist
    function whitelistAccount(address account) external;

    /// @notice Unallow an account to deposit tokens for rewarding
    /// @param account The address of the account to unwhitelist
    function unWhitelistAccount(address account) external;

    /// @notice Pauses the contract
    function pause() external;

    /// @notice Unpauses the contract
    function unpause() external;

    /// @notice Whitelisted uer function to deposit tokens for rewarding
    /// @param depositAmount The amount deposited
    function deposit(uint256 depositAmount) external;

    /// @notice Admin function to withdraw tokens
    /// @param amount The amount of tokens to withdraw
    /// @param to recipient of the tokens
    function withdraw(address to, uint256 amount) external;

    /// @notice Returns the ICNT token address
    function icnToken() external view returns (IERC20);
}
