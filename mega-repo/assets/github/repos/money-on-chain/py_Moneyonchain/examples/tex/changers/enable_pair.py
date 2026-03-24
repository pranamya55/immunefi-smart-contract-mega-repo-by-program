"""
Changer to change the enable a token pair in the MoC Decentralized Exchange
"""

import os
import json

from moneyonchain.manager import ConnectionManager
from moneyonchain.changers import DexTokenPairEnabler

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

contract = DexTokenPairEnabler(connection_manager)

# load settings from file
settings = options_from_settings(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'))


base_address = settings[network]['DOC']
secondary_address = settings[network]['BPRO']

tx_hash, tx_receipt = contract.constructor(base_address,
                                           secondary_address,
                                           execute_change=False)
if tx_receipt:
    print("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))
else:
    print("Error deploying changer")

"""

"""