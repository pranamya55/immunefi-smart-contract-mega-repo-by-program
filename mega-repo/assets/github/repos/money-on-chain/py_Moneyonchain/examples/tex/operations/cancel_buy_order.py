"""

cancels the buy _orderId order.
the contract must not be paused; the caller should be the order owner
_baseToken Base Token involved in the canceled Order pair
_secondaryToken Secondary Token involved in the canceled Order pair
_orderId Order id to cancel
_previousOrderIdHint previous order in the orderbook, used as on optimization to search for.

"""

import json
import os

from moneyonchain.networks import NetworkManager
from moneyonchain.tex import MoCDecentralizedExchange

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/cancel_buy_order.log',
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


# load settings from file
settings = options_from_settings(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'))

# instantiate DEX Contract
dex = MoCDecentralizedExchange(network_manager).from_abi()

base_token = settings[config_network]['DOC']
secondary_token = settings[config_network]['ADOC']
order_id = 140
previous_order_id = 0

print("Order cancel. Please wait to the transaction be mined!...")
tx_receipt = dex.cancel_buy_order(
    base_token,
    secondary_token,
    order_id,
    previous_order_id)

# finally disconnect from network
network_manager.disconnect()
