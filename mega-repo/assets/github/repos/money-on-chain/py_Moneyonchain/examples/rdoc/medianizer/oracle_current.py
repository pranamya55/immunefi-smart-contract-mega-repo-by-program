from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoCState

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()

connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_state = RDOCMoCState(network_manager).from_abi()
print(moc_state.price_provider())

# finally disconnect from network
network_manager.disconnect()
