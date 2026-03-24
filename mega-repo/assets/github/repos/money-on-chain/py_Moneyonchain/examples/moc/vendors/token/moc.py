from moneyonchain.networks import network_manager
from moneyonchain.tokens import MoCToken

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()

connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


token_moc = MoCToken(network_manager).from_abi()

print("Token Name: {}".format(token_moc.name()))
account_address = '0xB5E2Bed9235b6366Fa0254c2e6754E167e0a2383'
print("Account address:{}".format(account_address))
print("Token Balance:{}".format(token_moc.balance_of(account_address)))

# finally disconnect from network
network_manager.disconnect()
