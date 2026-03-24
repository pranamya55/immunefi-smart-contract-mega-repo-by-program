from moneyonchain.networks import network_manager
from moneyonchain.medianizer import MoCMedianizer, MoCGovernedAuthority

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()


connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

oracle_address = '0xe2927A0620b82A66D67F678FC9b826B0E01B1bFD'

# 3881519
oracle = MoCMedianizer(network_manager, contract_address=oracle_address).from_abi()
print(oracle.peek())


# finally disconnect from network
network_manager.disconnect()
