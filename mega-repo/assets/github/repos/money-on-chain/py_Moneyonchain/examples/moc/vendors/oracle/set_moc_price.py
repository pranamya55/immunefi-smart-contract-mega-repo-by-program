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

This is MoC Oracle price

"""

from moneyonchain.networks import network_manager
from moneyonchain.medianizer import MoCMedianizer, \
    PriceFeed

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha3'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)


oracle_address = '0xE972c8E83A5b97bB4FC867855A0aA13EF96f228D'
price_feeder = '0xB1F83adfC85125341f4576ef93C7B70C7E47697C'

oracle = MoCMedianizer(network_manager,
                       contract_address=oracle_address).from_abi()

feeder = PriceFeed(network_manager,
                   contract_address=price_feeder,
                   contract_address_moc_medianizer=oracle_address).from_abi()

feeder.post(1 * 10 ** 18, block_expiration=1000000)
print(feeder.zzz())
print(feeder.peek())

# finally disconnect from network
network_manager.disconnect()
