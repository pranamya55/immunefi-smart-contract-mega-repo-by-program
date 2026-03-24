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

# Owner: 0xB7d4B3c37d17D66B88da41e8A87561323A6DBDA0
oracle_address = '0x4A4D3130905Ec11C648D10EA494a0F0FD95a13Ad'
price_feeder = '0xD628179e15b51287271Eb73ee961b1da11A31cF9'

oracle = MoCMedianizer(network_manager,
                       contract_address=oracle_address).from_abi()

feeder = PriceFeed(network_manager,
                   contract_address=price_feeder,
                   contract_address_moc_medianizer=oracle_address).from_abi()

feeder.post(47000 * 10 ** 18, block_expiration=1000000)
print(feeder.zzz())
print(feeder.peek())

# finally disconnect from network
network_manager.disconnect()
