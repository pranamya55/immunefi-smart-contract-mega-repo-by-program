"""
Withdraws all the already charged(because of a matching, a cancellation or an expiration)
commissions of a given token
token Address of the token to withdraw the commissions from
"""

from decimal import Decimal
from web3 import Web3
import json
import os

from moneyonchain.networks import network_manager
from moneyonchain.tex import MoCDecentralizedExchange

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/withdraw.log',
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


connection_network = 'rskMainnetPublic'
config_network = 'dexMainnet'

log.info("Connecting to {0}".format(config_network))

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


# load settings from file
settings = options_from_settings(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'))

# instantiate DEX Contract
dex = MoCDecentralizedExchange(network_manager).from_abi()

token_name = 'WRBTC'
token = settings[config_network][token_name]

log.info("Withdraw commission from token: [{0}] {1}. Please wait to the transaction be mined!...".format(
    token_name,
    token
))
tx_receipt = dex.withdraw_commissions(
    token)


# finally disconnect from network
network_manager.disconnect()
