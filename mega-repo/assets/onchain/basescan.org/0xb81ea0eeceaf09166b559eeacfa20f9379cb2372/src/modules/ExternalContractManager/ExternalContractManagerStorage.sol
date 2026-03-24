// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

import {IICNLink} from "../../common/interfaces/IICNLink.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ReservePoolV2 as ReservePool} from "../../reservePool/v2/ReservePoolV2.sol";
import {TreasuryV2 as Treasury} from "../../treasury/v2/TreasuryV2.sol";

contract ExternalContractManagerStorage {
    /// @custom:storage-location erc7201:externalcontractmanager.storage
    struct ExternalContractManagerStorageData {
        uint64 version;
        IICNLink icnLink;
        IERC20 icnToken;
        ReservePool reserve;
        Treasury treasury;
    }

    // keccak256(abi.encode(uint256(keccak256("externalcontractmanager.storage")) - 1)) & ~bytes32(uint256(0xff));
    bytes32 internal constant EXTERNAL_CONTRACT_MANAGER_STORAGE_SLOT =
        0x35c1414fbb55cef723c681079e3c57746b031e3ba1a9238e3fda82702db24700;

    function _setICNLink(address icnLink) internal {
        ExternalContractManagerStorageData storage $ = getExternalContractManagerStorage();
        $.icnLink = IICNLink(icnLink);
    }

    function _setICNToken(address icnToken) internal {
        ExternalContractManagerStorageData storage $ = getExternalContractManagerStorage();
        $.icnToken = IERC20(icnToken);
    }

    function _setReserve(address reserve) internal {
        ExternalContractManagerStorageData storage $ = getExternalContractManagerStorage();
        $.reserve = ReservePool(reserve);
    }

    function _setTreasury(address treasury) internal {
        ExternalContractManagerStorageData storage $ = getExternalContractManagerStorage();
        $.treasury = Treasury(treasury);
    }

    function getExternalContractManagerStorage() internal pure returns (ExternalContractManagerStorageData storage $) {
        bytes32 slot = EXTERNAL_CONTRACT_MANAGER_STORAGE_SLOT;
        assembly {
            $.slot := slot
        }
    }
}
