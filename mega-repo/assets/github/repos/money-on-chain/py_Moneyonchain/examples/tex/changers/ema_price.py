"""
Ema Price Changer
"""

import json
import os
from decimal import Decimal

from moneyonchain.manager import ConnectionManager
from moneyonchain.changers import DexEMAPriceChanger

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger('default')


def options_from_settings(filename='settings.json'):
    """ Options from file settings.json """

    with open(filename) as f:
        config_options = json.load(f)

    return config_options


network = 'dexTestnet'
connection_manager = ConnectionManager(network=network)
print("Connecting to %s..." % network)
print("Connected: {conectado}".format(conectado=connection_manager.is_connected))

contract = DexEMAPriceChanger(connection_manager)

# load settings from file
settings = options_from_settings(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'))


base_token = settings[network]['DOC']
secondary_token = settings[network]['RIF']
ema_price = int(Decimal(0.1033) * 10 ** 18)

tx_hash, tx_receipt = contract.constructor(base_token,
                                           secondary_token,
                                           ema_price,
                                           execute_change=False)
if tx_receipt:
    print("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))
else:
    print("Error deploying changer")

"""

"""