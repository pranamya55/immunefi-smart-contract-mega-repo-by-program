from moneyonchain.networks import NetworkManager
from moneyonchain.oracle import PriceProvider

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()

connection_network='rskTestnetPublic'
config_network = 'rdocTestnet'

# init network manager
# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager = NetworkManager(
    connection_network=connection_network,
    config_network=config_network)

# run install() if is the first time and you want to install
# networks connection from brownie
# network_manager.install()

# Connect to network
network_manager.connect()

price_provider = PriceProvider(network_manager)

log.info("Last price: {0}".format(price_provider.price()))

# finally disconnect from network
network_manager.disconnect()
