from moneyonchain.networks import network_manager
from moneyonchain.medianizer import RDOCMoCMedianizer

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


#oracle_address = '0x2B54819531B7126bDEE2CeFDD9c5342d6c307595'
#oracle_address = '0x01a165cC33Ff8Bd0457377379962232886be3DE6'
#oracle_address = '0x9d4b2c05818A0086e641437fcb64ab6098c7BbEc'
#oracle_address = '0x9315AFD6aEc0bb1C1FB3fdcdC2E43797B0A61853'
#oracle_address = '0xb856Ca7c722cfb202D81c55DC7925e02ed3f0A2F'
#oracle_address = '0xCEE08e06617f8b5974Db353E2c8C66424F91c42A'
#oracle_address = '0x9d4b2c05818A0086e641437fcb64ab6098c7BbEc'
oracle_address = '0xb8deE36b3488E205aB8E5Fd2502e4104917F46FF'

oracle = RDOCMoCMedianizer(network_manager, contract_address=oracle_address).from_abi()
#print(oracle.price())
print(oracle.peek())

# finally disconnect from network
network_manager.disconnect()
