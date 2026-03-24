"""
Changer Max Order lifespan
"""

from moneyonchain.networks import NetworkManager
from moneyonchain.tex import DexMaxOrderLifespanChanger

# Logging setup

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/max_order_lifespan.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network = 'rskTestnetPublic'
config_network = 'dexTestnet'

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

# instantiate Changer
changer = DexMaxOrderLifespanChanger(network_manager, logger=log)

max_order_life_span = 7000

tx_receipt = changer.constructor(max_order_life_span, execute_change=False)

# finally disconnect from network
network_manager.disconnect()
