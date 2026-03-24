"""
Inserts an order in the buy orderbook of a given pair without a hint
the pair should not be disabled; the contract should not be paused. Takes the funds
with a transferFrom


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

"""

import json
import os
import logging

from moneyonchain.networks import NetworkManager
from moneyonchain.tex import MoCDecentralizedExchange

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/insert_sell_market_order.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


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

# instantiate TEX Contract
dex = MoCDecentralizedExchange(network_manager).from_abi()

base_token = settings[config_network]['WRBTC']
secondary_token = settings[config_network]['AMOC']
amount = 0.001
multiply_factor = 1.01
lifespan = 2

print("Insert sell market order. Please wait to the transaction be mined!...")
tx_receipt = dex.insert_sell_market_order(
    base_token,
    secondary_token,
    amount,
    multiply_factor,
    lifespan)

# finally disconnect from network
network_manager.disconnect()
