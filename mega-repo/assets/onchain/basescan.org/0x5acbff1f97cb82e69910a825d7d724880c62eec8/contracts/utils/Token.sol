// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts-upgradeable/token/ERC20/ERC20Upgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/utils/PausableUpgradeable.sol";
import "@openzeppelin/contracts/proxy/utils/UUPSUpgradeable.sol";

contract MyToken is ERC20Upgradeable, AccessControlUpgradeable, PausableUpgradeable, UUPSUpgradeable {
    uint8 private immutable _decimals;

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant GUARDIAN_ROLE = keccak256("GUARDIAN_ROLE");

    mapping(address => bool) private _blacklist;

    constructor (uint8 __decimals) {
        _decimals = __decimals;
    }

    function decimals() public view override returns (uint8) {
        return _decimals;
    }

    function initialize(string memory name, string memory symbol, address admin) public initializer {
        __ERC20_init(name, symbol);
        __Pausable_init();

        _grantRole(DEFAULT_ADMIN_ROLE, admin);
    }

    function _authorizeUpgrade(address newImplementation) internal override onlyRole(DEFAULT_ADMIN_ROLE) {}


    // blacklist
    function blacklist(address account) external onlyRole(DEFAULT_ADMIN_ROLE) {
        _blacklist[account] = true;
        emit Blacklisted(account);
    }

    function unblacklist(address account) external onlyRole(DEFAULT_ADMIN_ROLE) {
        _blacklist[account] = false;
        emit Unblacklisted(account);
    }

    modifier notBlacklisted(address account) {
        require(!_blacklist[account], "Address is blacklisted");
        _;
    }

    event Blacklisted(address indexed account);
    event Unblacklisted(address indexed account);


    // minter
    function grantMinterRole(address account) external onlyRole(DEFAULT_ADMIN_ROLE) {
        grantRole(MINTER_ROLE, account);
    }

    function revokeMinterRole(address account) external onlyRole(DEFAULT_ADMIN_ROLE) {
        revokeRole(MINTER_ROLE, account);
    }

    function renounceMinterRole() external onlyRole(MINTER_ROLE) {
        renounceRole(MINTER_ROLE, _msgSender());
    }

    function mint(address to, uint256 amount) external onlyRole(MINTER_ROLE) {
        require(!_blacklist[to], "Recipient is blacklisted");
        _mint(to, amount);
    }

    function burn(uint256 amount) external onlyRole(MINTER_ROLE) {
        _burn(_msgSender(), amount);
    }


    // guardian
    function grantGuardianRole(address account) external onlyRole(DEFAULT_ADMIN_ROLE) {
        grantRole(GUARDIAN_ROLE, account);
    }

    function revokeGuardianRole(address account) external onlyRole(DEFAULT_ADMIN_ROLE) {
        revokeRole(GUARDIAN_ROLE, account);
    }

    function renounceGuardianRole() external onlyRole(GUARDIAN_ROLE) {
        renounceRole(GUARDIAN_ROLE, _msgSender());
    }

    function pause() external onlyRole(GUARDIAN_ROLE) {
        _pause();
    }

    function unpause() external onlyRole(GUARDIAN_ROLE) {
        _unpause();
    }


    // ERC20 methods
    function transfer(
        address recipient,
        uint256 amount
    ) public override notBlacklisted(_msgSender()) notBlacklisted(recipient) whenNotPaused returns (bool) {
        return super.transfer(recipient, amount);
    }

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) public override notBlacklisted(sender) notBlacklisted(recipient) whenNotPaused returns (bool) {
        return super.transferFrom(sender, recipient, amount);
    }

    function approve(
        address spender,
        uint256 amount
    ) public override notBlacklisted(_msgSender()) notBlacklisted(spender) whenNotPaused returns (bool) {
        return super.approve(spender, amount);
    }
}
