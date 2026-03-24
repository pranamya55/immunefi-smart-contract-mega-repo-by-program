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


from moneyonchain.networks import network_manager
from moneyonchain.moc_vendors import VENDORSMoC

connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha3'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_main = VENDORSMoC(network_manager, load_sub_contract=False).from_abi().contracts_discovery()

print(moc_main.sc_moc_moc_token.address())

print(moc_main.sc_moc_vendors.address())

# finally disconnect from network
network_manager.disconnect()
