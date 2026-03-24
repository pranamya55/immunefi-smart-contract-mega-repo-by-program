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
from moneyonchain.moc_vendors import VENDORSMoCState, \
    VENDORSMoCInrate, VENDORSMoCVendors, VENDORSMoCExchange


connection_network='rskTestnetPublic'
config_network = 'mocTestnetAlpha3'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_state = VENDORSMoCState(network_manager).from_abi()
moc_inrate = VENDORSMoCInrate(network_manager).from_abi()
moc_vendors = VENDORSMoCVendors(network_manager).from_abi()
moc_exchange = VENDORSMoCExchange(network_manager).from_abi()

print("MoC price:")
print(moc_state.moc_price())

vendor_address = Web3.toChecksumAddress('0x9032f510a5b54a005f04e81b5c98b7f201c4dac1')
amount = 0.3
result = moc_inrate.calculate_vendor_markup(vendor_address, amount)
print("Vendor markup: ", result)
print("Is expected: ", result == 0.003)

balance = moc_exchange.moc_token_balance(vendor_address, moc_vendors.address())
print("Balance and allowance: ", balance)

tx_type_mint_bpro_fees_rbtc = moc_inrate.tx_type_mint_bpro_fees_rbtc()
tx_type_mint_bpro_fees_moc = moc_inrate.tx_type_mint_bpro_fees_moc()
#commissions = moc_exchange.calculate_commissions_with_prices(
#    amount, tx_type_mint_bpro_fees_moc, tx_type_mint_bpro_fees_rbtc, vendor_address)
#print("Commissions: ", commissions)


# finally disconnect from network
network_manager.disconnect()
