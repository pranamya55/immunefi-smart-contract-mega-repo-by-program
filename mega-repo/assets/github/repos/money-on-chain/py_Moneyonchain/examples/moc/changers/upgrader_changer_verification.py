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
from moneyonchain.governance import UpgraderChanger

connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)

upgrader_changer_address = Web3.toChecksumAddress('0x76cd9670E063681780886256136Ae86fA7cB05C9')
upgrader_changer = UpgraderChanger(network_manager,
                                   contract_address=upgrader_changer_address).from_abi()

print("Proxy Address: {0}".format(upgrader_changer.proxy()))
print("Upgrade Delegator: {0}".format(upgrader_changer.upgrade_delegator()))
print("New implementation address: {0}".format(upgrader_changer.new_implementation()))



