// SPDX-License-Identifier: BUSL-1.1
/*
      ▄▄█████████▄
   ╓██▀└ ,╓▄▄▄, '▀██▄
  ██▀ ▄██▀▀╙╙▀▀██▄ └██µ           ,,       ,,      ,     ,,,            ,,,
 ██ ,██¬ ▄████▄  ▀█▄ ╙█▄      ▄███▀▀███▄   ███▄    ██  ███▀▀▀███▄    ▄███▀▀███,
██  ██ ╒█▀'   ╙█▌ ╙█▌ ██     ▐██      ███  █████,  ██  ██▌    └██▌  ██▌     └██▌
██ ▐█▌ ██      ╟█  █▌ ╟█     ██▌      ▐██  ██ └███ ██  ██▌     ╟██ j██       ╟██
╟█  ██ ╙██    ▄█▀ ▐█▌ ██     ╙██      ██▌  ██   ╙████  ██▌    ▄██▀  ██▌     ,██▀
 ██ "██, ╙▀▀███████████⌐      ╙████████▀   ██     ╙██  ███████▀▀     ╙███████▀`
  ██▄ ╙▀██▄▄▄▄▄,,,                ¬─                                    '─¬
   ╙▀██▄ '╙╙╙▀▀▀▀▀▀▀▀
      ╙▀▀██████R⌐
 */
pragma solidity 0.8.16;

interface IBaseRWAManagerErrors {
  /// Error emitted when the token address is zero
  error TokenAddressCantBeZero();

  /// Error emitted when the token is not accepted for subscription
  error TokenNotAccepted();

  /// Error emitted when the deposit amount is too small
  error DepositAmountTooSmall();

  /// Error emitted when rwa amount is below the `minimumRwaReceived` in a subscription
  error RwaReceiveAmountTooSmall();

  /// Error emitted when the user is not registered with the ID registry
  error UserNotRegistered();

  /// Error emitted when the redemption amount is too small
  error RedemptionAmountTooSmall();

  /// Error emitted when the receive amount is below the `minimumReceiveAmount` in a redemption
  error ReceiveAmountTooSmall();

  /// Error emitted when attempting to set the `OndoTokenRouter` address to zero
  error RouterAddressCantBeZero();

  /// Error emitted when attempting to set the `OndoOracle` address to zero
  error OracleAddressCantBeZero();

  /// Error emitted when attempting to set the `OndoCompliance` address to zero
  error ComplianceAddressCantBeZero();

  /// Error emitted when attempting to set the `OndoIDRegistry` address to zero
  error IDRegistryAddressCantBeZero();

  /// Error emitted when attempting to set the `OndoRateLimiter` address to zero
  error RateLimiterAddressCantBeZero();

  /// Error emitted when attempting to set the `OndoFees` address to zero
  error FeesAddressCantBeZero();

  /// Error emitted when attempting to set the `AdminSubscriptionChecker` address to zero
  error AdminSubscriptionCheckerAddressCantBeZero();

  /// Error emitted when the price of RWA token returned from the oracle is below the minimum price
  error RWAPriceTooLow();

  /// Error emitted when the subscription functionality is paused
  error SubscriptionsPaused();

  /// Error emitted when the redemption functionality is paused
  error RedemptionsPaused();

  /// Error emitted when the fee is greater than the redemption amount
  error FeeGreaterThanRedemption();

  /// Error emitted when the fee is greater than the subscription amount
  error FeeGreaterThanSubscription();
}
