"""
If is the first time to py_Moneyonchain we need brownie framework installed

`pip install eth-brownie==1.12.2`

and to install connection nodes required to connect, also run :

```
console> brownie networks add RskNetwork rskTestnetPublic host=https://public-node.testnet.rsk.co chainid=31 explorer=https://blockscout.com/rsk/mainnet/api
console> brownie networks add RskNetwork rskTestnetLocal host=http://localhost:4444 chainid=31 explorer=https://blockscout.com/rsk/mainnet/api
console> brownie networks add RskNetwork rskMainnetPublic host=https://public-node.rsk.co chainid=30 explorer=https://blockscout.com/rsk/mainnet/api
console> brownie networks add RskNetwork rskMainnetLocal host=http://localhost:4444 chainid=30 explorer=https://blockscout.com/rsk/mainnet/api
```

"""

from web3 import Web3

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoCState


connection_network='rskMainnetPublic'
config_network = 'mocMainnet2'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_state = MoCState(network_manager).from_abi()

bucket_x2 = moc_state.bucket_x2()
bucket_c0 = moc_state.bucket_c0()

print("Price Provider: {0}".format(moc_state.price_provider()))
print("Bitcoin Price in USD: {0}".format(moc_state.bitcoin_price()))
print("Bitcoin Moving Average in USD: {0}".format(moc_state.bitcoin_moving_average()))
print("Days to settlement: {0}".format(moc_state.days_to_settlement()))
print("Global Coverage: {0}".format(moc_state.global_coverage()))
print("Bitpro Total Supply: {0}".format(moc_state.bitpro_total_supply()))
print("DOC Total Supply: {0}".format(moc_state.doc_total_supply()))
print("Implementation: {0}".format(moc_state.implementation()))
print("BPro Discount rate: {0}".format(moc_state.bpro_discount_rate()))
print("BPro Tec Price: {0}".format(moc_state.bpro_tec_price()))
print("Max BPro Discount: {0}".format(moc_state.max_bpro_with_discount()))
print("State: {0}".format(moc_state.state()))
print("RBTC in System: {0}".format(moc_state.rbtc_in_system()))
print("cobj: {0}".format(moc_state.cobj()))
print("cobjX: {0}".format(moc_state.cobj_X2()))
print("cobjX: {0}".format(moc_state.cobj_X2()))
print("MaxBProX: {0}".format(moc_state.max_bprox(bucket_x2)))
print("MaxBProX BTC Value: {0}".format(moc_state.max_bprox_btc_value()))
print("BproX Price: {0}".format(moc_state.bprox_price()))
print("BproX Tec Price: {0}".format(moc_state.btc2x_tec_price()))
print("Days to settlement: {0}".format(moc_state.days_to_settlement()))
print("coverage: {0}".format(moc_state.coverage(bucket_x2)))
print("Is Liquidation: {0}".format(moc_state.is_liquidation()))
print("Is calculated: {0}".format(moc_state.is_calculate_ema()))

print()
print("Vendors STATS:")
print("==============")
print("MoC Price: {0}".format(moc_state.moc_price()))
print("MoC Price Provider: {0}".format(moc_state.moc_price_provider()))
print("MoC Token: {0}".format(moc_state.moc_token()))
print("MoC Vendors: {0}".format(moc_state.moc_vendors()))
print("Protected: {0}".format(moc_state.protected()))
print("Liquidation enabled: {0}".format(moc_state.liquidation_enabled()))

# finally disconnect from network
network_manager.disconnect()
