// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

import {IEraManagerErrors} from "./IEraManagerErrors.sol";

/// @dev External interface of EraManagerStorage

interface IEraManagerStorage is IEraManagerErrors {
    struct EraSegment {
        uint256 eraNumber;
        uint256 startBlock;
        uint256 duration;
    }
}
