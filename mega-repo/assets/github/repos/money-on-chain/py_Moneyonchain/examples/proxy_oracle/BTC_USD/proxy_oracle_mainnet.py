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
config_network = 'proxyBTCUSDMainnet'

log.info("Connecting... Network: {0} Enviroment: {1}".format(connection_network, config_network))

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

oracle_address = '0x972a21C61B436354C0F35836195D7B67f54E482C'

oracle = ProxyMoCMedianizer(network_manager, contract_address=oracle_address).from_abi()
log.info("Medianizer: {0}".format(oracle.sc.medianizer()))
log.info("Price: {0} Valid: {1}".format(oracle.peek()[0], oracle.peek()[1]))


# finally disconnect from network
network_manager.disconnect()
