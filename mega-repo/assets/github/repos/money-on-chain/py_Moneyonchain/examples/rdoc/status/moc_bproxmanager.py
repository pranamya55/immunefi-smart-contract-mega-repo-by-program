from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoCBProxManager

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()


connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnetAlpha'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_bprox_manager = RDOCMoCBProxManager(network_manager).from_abi()

print("Available bucket: {0}".format(moc_bprox_manager.available_bucket()))
print("Active address count: {0}".format(moc_bprox_manager.active_address_count(block_identifier=2923911)))

# finally disconnect from network
network_manager.disconnect()