from moneyonchain.networks import network_manager
from moneyonchain.tokens import BProToken

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()

connection_network = 'rskTestnetPublic'
config_network = 'mocTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

ibpro_address = '0x6226b4b3f29ECB5F9eEC3ec3391488173418DD5d'
token = BProToken(network_manager, contract_address=ibpro_address).from_abi()

print(token.name())
print(token.symbol())
print(token.total_supply())
print(token.balance_of('0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3'))

# finally disconnect from network
network_manager.disconnect()


