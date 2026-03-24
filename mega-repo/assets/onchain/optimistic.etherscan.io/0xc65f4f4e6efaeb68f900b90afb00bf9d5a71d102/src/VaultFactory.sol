// SPDX-License-Identifier: BUSL-1.1
// SPDX-FileCopyrightText: 2024 Kiln <contact@kiln.fi>
//
// ██╗  ██╗██╗██╗     ███╗   ██╗
// ██║ ██╔╝██║██║     ████╗  ██║
// █████╔╝ ██║██║     ██╔██╗ ██║
// ██╔═██╗ ██║██║     ██║╚██╗██║
// ██║  ██╗██║███████╗██║ ╚████║
// ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═══╝
//
pragma solidity 0.8.22;

import {Create2} from "@openzeppelin/utils/Create2.sol";
import {AccessControlDefaultAdminRules} from "@openzeppelin/access/extensions/AccessControlDefaultAdminRules.sol";
import {IERC20} from "@openzeppelin/token/ERC20/IERC20.sol";

import {AddressNotContract} from "./Errors.sol";
import {IConnectorRegistry, ISanctionsList, Vault} from "./Vault.sol";
import {VaultBeaconProxy} from "./proxy/VaultBeaconProxy.sol";

/// @title Kiln DeFi Integration Vault Factory.
/// @notice Factory to deploy new Vaults and initialize them.
/// @author maximebrugel @ Kiln.
contract VaultFactory is AccessControlDefaultAdminRules {
    /* -------------------------------------------------------------------------- */
    /*                                  CONSTANTS                                 */
    /* -------------------------------------------------------------------------- */

    /// @notice The role code for the deployer role.
    bytes32 public constant DEPLOYER_ROLE = bytes32("DEPLOYER");

    /* -------------------------------------------------------------------------- */
    /*                                  IMMUTABLE                                 */
    /* -------------------------------------------------------------------------- */

    /// @notice The beacon used to create new vaults.
    address public immutable vaultBeacon;

    /// @notice The connector registry used to create new vaults.
    IConnectorRegistry public immutable connectorRegistry;

    /* -------------------------------------------------------------------------- */
    /*                                   STORAGE                                  */
    /* -------------------------------------------------------------------------- */

    /// @notice The list of deployed vaults.
    Vault[] public deployedVaults;

    /* -------------------------------------------------------------------------- */
    /*                                   EVENTS                                   */
    /* -------------------------------------------------------------------------- */

    /// @dev Emitted when a new vault is created.
    /// @param vault The address of the new vault.
    /// @param name The name of the new vault.
    event VaultCreated(address indexed vault, string name);

    /* -------------------------------------------------------------------------- */
    /*                                 CONSTRUCTOR                                */
    /* -------------------------------------------------------------------------- */

    constructor(
        address _initialAdmin,
        address _initialDeployer,
        uint48 _initialDelay,
        address _vaultBeacon,
        address _connectorRegistry
    ) AccessControlDefaultAdminRules(_initialDelay, _initialAdmin) {
        if (_vaultBeacon.code.length == 0) revert AddressNotContract(_vaultBeacon);
        vaultBeacon = _vaultBeacon;

        if (_connectorRegistry.code.length == 0) revert AddressNotContract(_connectorRegistry);
        connectorRegistry = IConnectorRegistry(_connectorRegistry);
        _grantRole(DEPLOYER_ROLE, _initialDeployer);
    }

    /* -------------------------------------------------------------------------- */
    /*                                FACTORY LOGIC                               */
    /* -------------------------------------------------------------------------- */

    /// @notice The parameters to create a new vault.
    struct CreateVaultParams {
        IERC20 asset_;
        string name_;
        string symbol_;
        bool transferable_;
        bytes32 connectorName_;
        Vault.FeeRecipient[] recipients_;
        uint256 managementFee_;
        uint256 performanceFee_;
        address initialDefaultAdmin_;
        address initialFeeManager_;
        address initialSanctionsManager_;
        address initialClaimManager_;
        address initialPauser_;
        address initialUnpauser_;
        uint48 initialDelay_;
        uint8 offset_;
        ISanctionsList sanctionsList_;
        uint256 minTotalSupply_;
    }

    /// @notice Creates a new vault.
    /// @param params The parameters to initialize the vault.
    /// @param salt The salt for the Vault deployment with CREATE2.
    /// @return The address of the new vault.
    function createVault(CreateVaultParams memory params, bytes32 salt)
        external
        onlyRole(DEPLOYER_ROLE)
        returns (address)
    {
        Vault.InitializationParams memory initializationParams = Vault.InitializationParams({
            asset_: params.asset_,
            name_: params.name_,
            symbol_: params.symbol_,
            transferable_: params.transferable_,
            connectorName_: params.connectorName_,
            connectorRegistry_: connectorRegistry,
            recipients_: params.recipients_,
            managementFee_: params.managementFee_,
            performanceFee_: params.performanceFee_,
            initialDefaultAdmin_: params.initialDefaultAdmin_,
            initialFeeManager_: params.initialFeeManager_,
            initialSanctionsManager_: params.initialSanctionsManager_,
            initialClaimManager_: params.initialClaimManager_,
            initialPauser_: params.initialPauser_,
            initialUnpauser_: params.initialUnpauser_,
            initialDelay_: params.initialDelay_,
            offset_: params.offset_,
            sanctionsList_: params.sanctionsList_,
            minTotalSupply_: params.minTotalSupply_
        });

        bytes memory _initCalldata = abi.encodeCall(Vault.initialize, initializationParams);

        address payable _newVault = payable(
            Create2.deploy(
                0, salt, abi.encodePacked(type(VaultBeaconProxy).creationCode, abi.encode(vaultBeacon, _initCalldata))
            )
        );

        deployedVaults.push(Vault(_newVault));
        emit VaultCreated(_newVault, params.name_);
        return _newVault;
    }
}
