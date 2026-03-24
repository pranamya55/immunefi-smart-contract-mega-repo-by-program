from moneyonchain.networks import network_manager
from moneyonchain.medianizer import ProxyMoCMedianizer

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()


connection_network = 'rskTestnetPublic'
config_network = 'proxyBTCUSDTestnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

oracle_address = '0xb76c405Dfd042D88FD7b8dd2e5d66fe7974A1458'

oracle = ProxyMoCMedianizer(network_manager, contract_address=oracle_address).from_abi()
log.info("Medianizer: {0}".format(oracle.sc.medianizer()))
log.info("Price: {0} Valid: {1}".format(oracle.peek()[0], oracle.peek()[1]))


# finally disconnect from network
network_manager.disconnect()
