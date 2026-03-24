from moneyonchain.networks import network_manager
from moneyonchain.medianizer import RDOCPriceFeed

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


#feeder_address = '0x652255254E79CD0954Bdd8B72ED00D9614Eba6A8'
#oracle_address = '0x2B54819531B7126bDEE2CeFDD9c5342d6c307595'

feeder_address = '0xe7295C7776Bf5f6a042bA009c41D9f900F8aE819'
oracle_address = '0x01a165cC33Ff8Bd0457377379962232886be3DE6'
feeder = RDOCPriceFeed(network_manager,
                       contract_address=feeder_address,
                       contract_address_moc_medianizer=oracle_address).from_abi()

# write price on price feeder
feeder.post(0.056 * 10 ** 18, block_expiration=300)
print(feeder.zzz())
print(feeder.peek())


# finally disconnect from network
network_manager.disconnect()
