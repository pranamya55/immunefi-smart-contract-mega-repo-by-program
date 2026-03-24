from moneyonchain.networks import network_manager
from moneyonchain.medianizer import RDOCPriceFeed, RDOCMoCMedianizer

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


oracle_address = '0x01a165cC33Ff8Bd0457377379962232886be3DE6'

oracle = RDOCMoCMedianizer(network_manager,
                           contract_address=oracle_address).from_abi()

print("Peek:")
print(oracle.peek())
print("Compute:")
print(oracle.compute())

if not oracle.compute()[1] and oracle.peek()[1]:
    print("Recalculating oracle status...")
    oracle.poke()
    print("Oracle status updated!")
else:
    print("Not time to recalculate status!")

# finally disconnect from network
network_manager.disconnect()
