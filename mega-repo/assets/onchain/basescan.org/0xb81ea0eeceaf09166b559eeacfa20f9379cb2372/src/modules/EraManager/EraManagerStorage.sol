// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

import {IEraManagerStorage} from "./interfaces/IEraManagerStorage.sol";

contract EraManagerStorage is IEraManagerStorage {
    /// @custom:storage-location erc7201:eramanager.storage
    struct EraManagerStorageData {
        uint64 version;
        EraSegment[] segments;
    }

    // keccak256(abi.encode(uint256(keccak256("eramanager.storage")) - 1)) & ~bytes32(uint256(0xff));
    bytes32 internal constant ERA_MANAGER_STORAGE_SLOT = 0xf886e8430ca15c92031e7db61db664bd2ff1d2dcc7694fd4b3fccfa95bbcc000;

    function _getEraManagerCurrentEra() internal view returns (uint256) {
        return _getEraManagerEraByBlock(block.number);
    }

    function _getEraManagerEraByBlock(uint256 bn) internal view returns (uint256 eraNumber) {
        EraManagerStorageData storage $ = getEraManagerStorage();

        require($.segments.length != 0, NoEraSegments());
        require(bn >= $.segments[0].startBlock, EraManagerInvalidArguments());

        for (uint256 i = $.segments.length; i != 0; i--) {
            EraSegment storage seg = $.segments[i - 1];

            if (bn >= seg.startBlock) {
                uint256 effTime = bn - seg.startBlock;
                uint256 erasPassed = effTime / seg.duration;
                return seg.eraNumber + erasPassed;
            }
        }
    }

    function getEraManagerStorage() internal pure returns (EraManagerStorageData storage $) {
        bytes32 slot = ERA_MANAGER_STORAGE_SLOT;
        assembly {
            $.slot := slot
        }
    }
}
