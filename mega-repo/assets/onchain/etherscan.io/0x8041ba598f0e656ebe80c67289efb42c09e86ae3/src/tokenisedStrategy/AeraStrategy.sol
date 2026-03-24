// SPDX-License-Identifier: AGPL-3.0
pragma solidity >=0.8.18;

import "./BaseHooks.sol";
import "./interfaces/IAeraVaultV2.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract AeraStrategy is BaseHooks, ReentrancyGuard {
  using SafeERC20 for IERC20;
  address public immutable vaultYearn; // vault that can call deposit/withdraw
  address public vaultAera; // Guantlet Vault
  address public quickManagement;
  address public pendingQuickManagement; // Address that is pending to take over `management`.

  event UpdateQuickManagement(address indexed newQuickManagement);
  event UpdateVaultAera(address indexed vaultAera);
  event UpdatePendingQuickManagement(address indexed pendingQuickManagement);

  constructor(
    address _asset,
    string memory _name,
    address _vaultAera,
    address _vaultYearn,
    address _quickManagement
  ) BaseHooks(_asset, _name) {
    require(_vaultAera != address(0), "ZERO ADDRESS");
    vaultAera = _vaultAera;
    require(_vaultYearn != address(0), "ZERO ADDRESS");
    vaultYearn = _vaultYearn;
    require(_quickManagement != address(0), "ZERO ADDRESS");
    quickManagement = _quickManagement;
    emit UpdateQuickManagement(_quickManagement);
    emit UpdateVaultAera(_vaultAera);
    IERC20(_asset).safeIncreaseAllowance(vaultAera, type(uint256).max);
  }

  modifier onlyQuickManagement() {
    requireQuickManagementOrManagement(msg.sender);
    _;
  }

  /*//////////////////////////////////////////////////////////////
                        AERA FUNCTIONS
    ///////////////////////////////////////////////////////////////*/

  function execute(
    address to,
    uint256 value,
    bytes calldata data
  ) external payable nonReentrant onlyManagement returns (bool, bytes memory) {
    (bool success, bytes memory result) = to.call{ value: value }(data);
    return (success, result);
  }

  function executeOnAera(Operation calldata operation) external onlyManagement {
    IAeraVaultV2(vaultAera).execute(operation);
  }

  function claim() external {
    IAeraVaultV2(vaultAera).claim();
  }

  function setGuardianAndFeeRecipient(address newGuardian, address newFeeRecipient) external onlyManagement {
    IAeraVaultV2(vaultAera).setGuardianAndFeeRecipient(newGuardian, newFeeRecipient);
  }

  function setHooks(address newHooks) external onlyManagement {
    IAeraVaultV2(vaultAera).setHooks(newHooks);
  }

  function finalize() external onlyManagement {
    IAeraVaultV2(vaultAera).finalize();
  }

  function pause() external onlyManagement {
    IAeraVaultV2(vaultAera).pause();
  }

  function resume() external onlyManagement {
    IAeraVaultV2(vaultAera).resume();
  }

  function transferOwnership(address newOwner) external onlyManagement {
    address _vaultAera = vaultAera;
    IERC20(asset).safeApprove(_vaultAera, 0);
    IAeraVaultV2(_vaultAera).transferOwnership(newOwner);
  }

  function acceptOwnership() external onlyManagement {
    IAeraVaultV2(vaultAera).acceptOwnership();
  }

  function depositAeraVault(uint256 amount) external onlyQuickManagement {
    require(asset.balanceOf(address(this)) >= amount, "AmountTooHigh");
    _deployFunds(amount);
  }
  function withdrawAeraVault(uint256 amount) external onlyQuickManagement {
    require(_getAssetBalance() >= amount, "AmountTooHigh");
    _freeFunds(amount);
  }

  // Setters
  function setVaultAera(address _vaultAera) external onlyManagement {
    require(IAeraVaultV2(vaultAera).value() == 0, "!Empty");
    _setVaultAera(_vaultAera);
  }
  function setForceVaultAera(address _vaultAera) external onlyManagement {
    _setVaultAera(_vaultAera);
  }

  function setPendingQuickManagement(address _pendingQuickManagement) external onlyManagement {
    require(_pendingQuickManagement != address(0), "ZERO ADDRESS");
    pendingQuickManagement = _pendingQuickManagement;

    emit UpdatePendingQuickManagement(_pendingQuickManagement);
  }

  function acceptQuickManagement() external {
    require(msg.sender == pendingQuickManagement, "!pending");
    quickManagement = msg.sender;
    pendingQuickManagement = address(0);

    emit UpdateQuickManagement(msg.sender);
  }

  // Getters

  function availableWithdrawLimit(address) public view override returns (uint256) {
    return asset.balanceOf(address(this));
  }

  function availableDepositLimit(address _owner) public view override returns (uint256) {
    if (_owner == vaultYearn) return type(uint256).max;
    return 0;
  }

  function requireQuickManagementOrManagement(address _sender) public view {
    require(_sender == quickManagement || _sender == TokenizedStrategy.management(), "!quickManagement");
  }

  // Internal Functions

  function _preDepositHook(uint256, uint256, address receiver) internal view override {
    require(msg.sender == receiver, "!msg.sender");
  }

  function _deployFunds(uint256 _amount) internal override {
    AssetValue[] memory amounts = new AssetValue[](1);
    amounts[0] = AssetValue(asset, _amount);
    IAeraVaultV2(vaultAera).deposit(amounts);
  }

  function _freeFunds(uint256 _amount) internal override {
    AssetValue[] memory amounts = new AssetValue[](1);
    amounts[0] = AssetValue(asset, _amount);
    IAeraVaultV2(vaultAera).withdraw(amounts);
  }

  function _harvestAndReport() internal view override returns (uint256 _totalAssets) {
    _totalAssets = asset.balanceOf(address(this)) + IAeraVaultV2(vaultAera).value();
  }

  function _setVaultAera(address _vaultAera) internal {
    IERC20(asset).safeApprove(vaultAera, 0);
    vaultAera = _vaultAera;
    IERC20(asset).safeIncreaseAllowance(_vaultAera, type(uint256).max);
    emit UpdateVaultAera(_vaultAera);
  }

  function _getAssetBalance() internal view returns (uint256) {
    AssetValue[] memory assetAmounts = IAeraVaultV2(vaultAera).holdings();

    uint256 lenAssetAmounts = assetAmounts.length;

    for (uint256 i; i < lenAssetAmounts; ++i) {
      if (address(asset) == address(assetAmounts[i].asset)) {
        return assetAmounts[i].value;
      }
    }
    return 0;
  }
}
