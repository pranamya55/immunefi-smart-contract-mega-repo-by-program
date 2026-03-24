from moneyonchain.networks import network_manager
from moneyonchain.medianizer import ProxyMoCMedianizer

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()


connection_network = 'rskMainnetPublic'
config_network = 'ethMainnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

oracle_address = '0x84c260568cFE148dBcFb4C8cc62C4e0b6d998F91'

oracle = ProxyMoCMedianizer(network_manager, contract_address=oracle_address).from_abi()
log.info(oracle.price())
log.info(oracle.governor())


# finally disconnect from network
network_manager.disconnect()
