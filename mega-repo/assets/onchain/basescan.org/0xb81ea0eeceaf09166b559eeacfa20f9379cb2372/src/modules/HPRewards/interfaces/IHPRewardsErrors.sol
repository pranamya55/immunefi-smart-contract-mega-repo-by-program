// SPDX-License-Identifier: MIT

pragma solidity 0.8.28;

interface IHPRewardsErrors {
    /// @dev Error triggered when the HPRewards contract is already initialized
    error HPRewardsAlreadyInitialized();

    /// @dev Error triggered when the HPRewards contract is already activated
    error HPRewardsAlreadyActivated();

    /// @dev Error triggered when the caller is not authorized to claim rewards
    /// @param _expectedHpId The expected HP ID
    /// @param _sender The sender address
    error UnauthorizedForClaimRewards(address _expectedHpId, address _sender);

    /// @dev Error triggered when the HP reward claim index is invalid
    error InvalidHPRewardsClaimIndex();

    /// @dev Error triggered when the claim is not unlocked
    /// @param _claimTimestamp The claim timestamp
    /// @param _currentTimestamp The current timestamp
    error ClaimNotUnlocked(uint256 _claimTimestamp, uint256 _currentTimestamp);

    /// @dev Error triggered when there are no unclaimed HP rewards
    error NoUnclaimedHpRewards();

    /// @dev Error triggered when the target capacity is not set
    /// @param _regionId The region ID
    /// @param _hwClass The hardware class
    error TargetCapacityNotSet(string _regionId, string _hwClass);

    /// @dev Error triggered when the market adjustment factor is not set
    /// @param _regionId The region ID
    /// @param _hwClass The hardware class
    error MarketAdjustmentFactorNotSet(string _regionId, string _hwClass);

    /// @dev Error triggered when trying to set a network collateral reward redirection ratio too high
    error NetworkCollateralRedirectionTooHigh();

    /// @dev Error triggered when the scaler node ID array length is invalid
    error InvalidScalerNodeIdsArray();
}
