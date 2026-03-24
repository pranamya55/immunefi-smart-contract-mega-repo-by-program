"""

MaxOrderLifespan is the maximum lifespan in ticks for an order

"""

import json
import os
from moneyonchain.networks import NetworkManager
from moneyonchain.tex import MoCDecentralizedExchange


def options_from_settings(filename='settings.json'):
    """ Options from file settings.json """

    with open(filename) as f:
        config_options = json.load(f)

    return config_options


connection_network='rskTestnetPublic'
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

# load settings from file
settings = options_from_settings(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'))

dex = MoCDecentralizedExchange(network_manager).from_abi()

print("Max Order Life Span: {0}".format(dex.max_order_lifespan()))

# finally disconnect from network
network_manager.disconnect()
