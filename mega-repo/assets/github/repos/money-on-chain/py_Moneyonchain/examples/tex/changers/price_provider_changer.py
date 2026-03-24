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

To run this script need private key, run this scripts with:

user> export ACCOUNT_PK_SECRET=PK
user> python ./mint_bpro.py

Where replace with your PK, and also you need to have funds in this account


Price provider changer
"""

from moneyonchain.networks import network_manager
from moneyonchain.tex import DexPriceProviderChanger

# Logging setup

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/price_provider_changer.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network = 'rskMainnetPublic'
config_network = 'dexMainnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


# base_token = '0x09b6ca5E4496238A1F176aEa6Bb607DB96c2286E'  # WRBTC
# secondary_token = '0x0399c7F7B37E21cB9dAE04Fb57E24c68ed0B4635'  # AMOC
# price_provider_address = '0x555B4d436e21a0E09B63d03A005F825402647c6d'  # WRBTC/AMOC


# base_token = '0x09b6ca5E4496238A1F176aEa6Bb607DB96c2286E'  # WRBTC
# secondary_token = '0x45a97b54021a3F99827641AFe1BFAE574431e6ab'  # MOC
# price_provider_address = '0xfa8673e6c5B5c3F6899a42A887D47bc027D902da'  # WRBTC/MOC


base_token = '0x967f8799aF07DF1534d48A95a5C9FEBE92c53ae0'  # WRBTC
secondary_token = '0x9AC7fE28967B30E3A4e6e03286d715b42B453D10'  # MOC
price_provider_address = '0x3aa536E39B38F01318f59a587AF2741BF8ad244c'  # WRBTC/MOC


contract = DexPriceProviderChanger(network_manager)

tx_receipt = contract.constructor(base_token,
                                  secondary_token,
                                  price_provider_address,
                                  execute_change=False)
if tx_receipt:
    print("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    print("Error deploying changer")


# finally disconnect from network
network_manager.disconnect()
