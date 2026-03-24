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


feeder_address1 = '0xe7295C7776Bf5f6a042bA009c41D9f900F8aE819'
feeder_address2 = '0x0c8F4e12820CA09a9Fba5E3a05e695e8E4C2bf0C'
oracle_address = '0x01a165cC33Ff8Bd0457377379962232886be3DE6'

feeder1 = RDOCPriceFeed(network_manager,
                        contract_address=feeder_address1,
                        contract_address_moc_medianizer=oracle_address).from_abi()

feeder2 = RDOCPriceFeed(network_manager,
                        contract_address=feeder_address2,
                        contract_address_moc_medianizer=oracle_address).from_abi()

#feeder1.post(0.052 * 10 ** 18, block_expiration=300)
#feeder2.post(0.058 * 10 ** 18, block_expiration=300)

print("Feeders")
print(feeder1.peek())
print(feeder2.peek())


oracle = RDOCMoCMedianizer(network_manager,
                           contract_address=oracle_address).from_abi()
print("Medianizer:")
#oracle.poke()
print(oracle.peek())
print(oracle.compute())

# finally disconnect from network
network_manager.disconnect()
