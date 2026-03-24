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
from moneyonchain.rdoc import RDOCMoCVendors

connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnetAlpha'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_vendors = RDOCMoCVendors(network_manager).from_abi()

account = '0xdda74880d638451e6d2c8d3fc19987526a7af730'
#account = '0xDda74880D638451e6D2c8D3fC19987526A7Af730'
markup = 0.0005
tx_receipt = moc_vendors.register(account, markup)
if tx_receipt:
    print("Vendor registered!")

# finally disconnect from network
network_manager.disconnect()
