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

interface IUSDY_InstantManager {
  function subscribe(
    address depositToken,
    uint256 depositAmount,
    uint256 minimumRwaReceived
  ) external returns (uint256 rwaAmountOut);

  function subscribeRebasingUSDY(
    address depositToken,
    uint256 depositAmount,
    uint256 minimumRwaReceived
  ) external returns (uint256 rusdyAmountOut);

  function adminSubscribe(
    address recipient,
    uint256 rwaAmount,
    bytes32 metadata
  ) external;

  function adminSubscribeRebasingUSDY(
    address recipient,
    uint256 rusdyAmount,
    bytes32 metadata
  ) external;

  function redeem(
    uint256 rwaAmount,
    address receivingToken,
    uint256 minimumTokenReceived
  ) external returns (uint256 receiveTokenAmount);

  function redeemRebasingUSDY(
    uint256 rwaAmount,
    address receivingToken,
    uint256 minimumTokenReceived
  ) external returns (uint256 receiveTokenAmount);
}
