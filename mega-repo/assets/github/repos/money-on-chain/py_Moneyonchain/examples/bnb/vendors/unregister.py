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
from moneyonchain.moc_vendors import VENDORSMoCVendors

connection_network = 'bscTestnetPrivate'
config_network = 'bnbTestnet'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_vendors = VENDORSMoCVendors(network_manager).from_abi()

account = '0x8Cd86FDA897E04FcbdCECB36F3D0fB0a4FAc2DaE'
tx_receipt = moc_vendors.unregister(account)
if tx_receipt:
    print("Vendor unregistered!")

# finally disconnect from network
network_manager.disconnect()
