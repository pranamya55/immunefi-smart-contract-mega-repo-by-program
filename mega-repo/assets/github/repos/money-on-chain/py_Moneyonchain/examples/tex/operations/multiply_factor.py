"""

Multiply factor:
    Minimum range avalaible price to be paid
    Maximum range avalaible price to be paid

(100 + priceDifference) / 100 = Multiply Factor

Examples:

     1% Multiply Factor:
       (100 + 1) / 100 = 1.01
    -1% Multiply Factor:
       (100 - 1 ) / 100 = 0.99

     10% Multiply Factor:
       (100 + 10) / 100 = 1.1
    -10% Multiply Factor:
       (100 - 10 ) / 100 = 0.9



Range:

  Min Multiply Factor: 0.01
  Max Multiply Factor: 1.99

  0.01 < Multiply Factor < 1.99

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

print("Min Multiply Factor: {0}".format(dex.min_multiply_factor()))
print("Max Multiply Factor: {0}".format(dex.max_multiply_factor()))

# finally disconnect from network
network_manager.disconnect()
