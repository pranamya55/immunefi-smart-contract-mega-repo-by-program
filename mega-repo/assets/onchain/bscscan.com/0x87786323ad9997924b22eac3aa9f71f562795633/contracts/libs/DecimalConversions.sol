// SPDX-License-Identifier: MIT
pragma solidity 0.8.22;

/**
 * @title DecimalConversions
 * @notice Library for handling a preset decimal conversion between shared and local decimals.
 */
library DecimalConversions {
    // @dev Sets an implicit cap on the amount of tokens,
    // over uint64.max() will need some sort of outbound cap / totalSupply cap.
    // Lowest common decimal denominator between chains.
    // Defaults to 6 decimal places to provide up to 18,446,744,073,709.551615 units (max uint64).
    // ie. 4 sharedDecimals would be 1,844,674,407,370,955.1615
    uint8 public constant SHARED_DECIMALS = 6;

    // @dev This library as is, assumes token contracts that are using it, contain 18 decimals as the local decimals
    uint8 public constant LOCAL_DECIMALS = 18;

    // @dev Provides a conversion rate between local and shared decimals.
    uint256 public constant DECIMAL_CONVERSION_RATE = 10 ** (LOCAL_DECIMALS - SHARED_DECIMALS);

    /**
     * @notice Internal function to remove dust from the given local decimal amount.
     * @param _amountLD The amount in local decimals.
     * @return amountLD The amount after removing dust.
     *
     * @dev Prevents the loss of dust when moving amounts between chains with different decimals.
     * @dev eg. uint(123) with a conversion rate of 100 becomes uint(100).
     */
    function removeDust(uint256 _amountLD) internal pure returns (uint256 amountLD) {
        return (_amountLD / DECIMAL_CONVERSION_RATE) * DECIMAL_CONVERSION_RATE;
    }

    /**
     * @notice Internal function to convert an amount from shared decimals into local decimals.
     * @param _amountSD The amount in shared decimals.
     * @return amountLD The amount in local decimals.
     */
    function toLD(uint64 _amountSD) internal pure returns (uint256 amountLD) {
        return _amountSD * DECIMAL_CONVERSION_RATE;
    }

    /**
     * @notice Internal function to convert an amount from local decimals into shared decimals.
     * @param _amountLD The amount in local decimals.
     * @return amountSD The amount in shared decimals.
     */
    function toSD(uint256 _amountLD) internal pure returns (uint64 amountSD) {
        return uint64(_amountLD / DECIMAL_CONVERSION_RATE);
    }
}
