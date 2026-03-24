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
from moneyonchain.moc_vendors import VENDORSMoCInrate


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_inrate = VENDORSMoCInrate(network_manager).from_abi()

vendor_account = Web3.toChecksumAddress('0xDda74880D638451e6D2c8D3fC19987526A7Af730')
amount = 1.0

print("Markup: {}".format(moc_inrate.calculate_vendor_markup(vendor_account, amount)))

tx_type = moc_inrate.tx_type_mint_bpro_fees_rbtc()
print("mint_bpro_fees_rbtc: {0}".format(moc_inrate.commission_rate_by_transaction_type(tx_type)))
tx_type = moc_inrate.tx_type_redeem_bpro_fees_rbtc()
print("redeem_bpro_fees_rbtc: {0}".format(moc_inrate.commission_rate_by_transaction_type(tx_type)))
tx_type = moc_inrate.tx_type_mint_doc_fees_rbtc()
print("mint_doc_fees_rbtc: {0}".format(moc_inrate.commission_rate_by_transaction_type(tx_type)))
tx_type = moc_inrate.tx_type_redeem_doc_fees_rbtc()
print("redeem_doc_fees_rbtc: {0}".format(moc_inrate.commission_rate_by_transaction_type(tx_type)))
tx_type = moc_inrate.tx_type_mint_btcx_fees_rbtc()
print("mint_btcx_fees_rbtc: {0}".format(moc_inrate.commission_rate_by_transaction_type(tx_type)))
tx_type = moc_inrate.tx_type_redeem_btcx_fees_rbtc()
print("redeem_btcx_fees_rbtc: {0}".format(moc_inrate.commission_rate_by_transaction_type(tx_type)))
tx_type = moc_inrate.tx_type_mint_bpro_fees_moc()
print("mint_bpro_fees_moc: {0}".format(moc_inrate.commission_rate_by_transaction_type(tx_type)))
tx_type = moc_inrate.tx_type_redeem_bpro_fees_moc()
print("redeem_bpro_fees_moc: {0}".format(moc_inrate.commission_rate_by_transaction_type(tx_type)))
tx_type = moc_inrate.tx_type_mint_doc_fees_moc()
print("mint_doc_fees_moc: {0}".format(moc_inrate.commission_rate_by_transaction_type(tx_type)))
tx_type = moc_inrate.tx_type_redeem_doc_fees_moc()
print("redeem_doc_fees_moc: {0}".format(moc_inrate.commission_rate_by_transaction_type(tx_type)))
tx_type = moc_inrate.tx_type_mint_btcx_fees_moc()
print("mint_btcx_fees_moc: {0}".format(moc_inrate.commission_rate_by_transaction_type(tx_type)))
tx_type = moc_inrate.tx_type_redeem_btcx_fees_moc()
print("redeem_btcx_fees_moc: {0}".format(moc_inrate.commission_rate_by_transaction_type(tx_type)))

# finally disconnect from network
network_manager.disconnect()
