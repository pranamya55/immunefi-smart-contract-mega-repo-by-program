// SPDX-License-Identifier: BUSL-1.1
pragma solidity >=0.8.18;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "src/tokenisedStrategy/interfaces/IAssetRegistry.sol";
import "src/tokenisedStrategy/interfaces/IHooks.sol";
import "src/tokenisedStrategy/Types.sol";

interface IAeraVaultV2 {
  /// FUNCTIONS ///

  /// @notice Deposit assets.
  /// @param amounts Assets and amounts to deposit.
  /// @dev MUST revert if not called by owner.
  function deposit(AssetValue[] memory amounts) external;

  /// @notice Withdraw assets.
  /// @param amounts Assets and amounts to withdraw.
  /// @dev MUST revert if not called by owner.
  function withdraw(AssetValue[] memory amounts) external;

  /// @notice Set current guardian and fee recipient.
  /// @param guardian New guardian address.
  /// @param feeRecipient New fee recipient address.
  /// @dev MUST revert if not called by owner.
  function setGuardianAndFeeRecipient(address guardian, address feeRecipient) external;

  /// @notice Sets the current hooks module.
  /// @param hooks New hooks module address.
  /// @dev MUST revert if not called by owner.
  function setHooks(address hooks) external;

  /// @notice Execute a transaction via the vault.
  /// @dev Execution still should work when vault is finalized.
  /// @param operation Struct details for target and calldata to execute.
  /// @dev MUST revert if not called by owner.
  function execute(Operation memory operation) external;

  /// @notice Terminate the vault and return all funds to owner.
  /// @dev MUST revert if not called by owner.
  function finalize() external;

  /// @notice Stops the guardian from submission and halts fee accrual.
  /// @dev MUST revert if not called by owner or guardian.
  function pause() external;

  /// @notice Resume fee accrual and guardian submissions.
  /// @dev MUST revert if not called by owner.
  function resume() external;

  /// @notice Submit a series of transactions for execution via the vault.
  /// @param operations Sequence of operations to execute.
  /// @dev MUST revert if not called by guardian.
  function submit(Operation[] memory operations) external;

  /// @notice Claim fees on behalf of a current or previous fee recipient.
  function claim() external;

  /// @notice Get the current guardian.
  /// @return guardian Address of guardian.
  function guardian() external view returns (address guardian);

  /// @notice Get the current fee recipient.
  /// @return feeRecipient Address of fee recipient.
  function feeRecipient() external view returns (address feeRecipient);

  /// @notice Get the current asset registry.
  /// @return assetRegistry Address of asset registry.
  function assetRegistry() external view returns (IAssetRegistry assetRegistry);

  /// @notice Get the current hooks module address.
  /// @return hooks Address of hooks module.
  function hooks() external view returns (IHooks hooks);

  /// @notice Get fee per second.
  /// @return fee Fee per second in 18 decimal fixed point format.
  function fee() external view returns (uint256 fee);

  /// @notice Get current balances of all assets.
  /// @return assetAmounts Amounts of registered assets.
  function holdings() external view returns (AssetValue[] memory assetAmounts);

  /// @notice Get current total value of assets in vault.
  /// @return value Current total value.
  function value() external view returns (uint256 value);

  function transferOwnership(address newOwner) external;

  function acceptOwnership() external;

  function owner() external view returns (address);
}
