from moneyonchain.networks import network_manager
from moneyonchain.medianizer import BNBMoCMedianizer, MoCGovernedAuthority

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()


connection_network = 'bscTestnet'
config_network = 'bnbAlphaTestnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

oracle_address = '0x6cf318ecf1Cd101755ccdA027B1D47B48b542cBA'


oracle = BNBMoCMedianizer(network_manager, contract_address=oracle_address).from_abi()
print(oracle.peek())

# finally disconnect from network
network_manager.disconnect()
