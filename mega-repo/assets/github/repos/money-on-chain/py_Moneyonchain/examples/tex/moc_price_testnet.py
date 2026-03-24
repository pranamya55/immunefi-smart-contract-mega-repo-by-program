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
from moneyonchain.tex import MoCDecentralizedExchange


connection_network = 'rskTestnetPublic'
config_network = 'dexTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

# ADOC (Alpha DoC https://alpha-tesnet.moneyonchain.com)
base_token = '0x489049c48151924c07F86aa1DC6Cc3Fea91ed963'

# AMOC (Alpha MoC https://alpha-tesnet.moneyonchain.com)
secondary_token = '0x0399c7F7B37E21cB9dAE04Fb57E24c68ed0B4635'

dex = MoCDecentralizedExchange(network_manager).from_abi()
pair = (base_token, secondary_token)

print(dex.last_closing_price(pair))


# finally disconnect from network
network_manager.disconnect()
