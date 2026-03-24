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

account_address = '0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3'
print("Account balance:{}".format(account_address))

ibpro_address = '0x6226b4b3f29ECB5F9eEC3ec3391488173418DD5d'
ibpro = BProToken(network_manager, contract_address=ibpro_address).from_abi()
ibpro_total_suply = ibpro.total_supply()
print("Token Name: {}".format(ibpro.name()))
print("Total supply:{}".format(ibpro_total_suply))
print(ibpro.balance_of(account_address))

bpro_address = '0x4dA7997A819bb46B6758b9102234c289Dd2ad3bf'
bpro = BProToken(network_manager, contract_address=bpro_address).from_abi()
print(bpro.name())
print(bpro.balance_of(ibpro_address))


# finally disconnect from network
network_manager.disconnect()


