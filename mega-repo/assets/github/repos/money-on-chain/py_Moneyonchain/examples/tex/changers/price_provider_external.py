"""
Price Provider Changer
"""
import json
import os

from moneyonchain.networks import network_manager
from moneyonchain.tex import ExternalOraclePriceProviderFallback, DexPriceProviderChanger

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


connection_network = 'rskTestnetPublic'
config_network = 'dexTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


# load settings from file
settings = options_from_settings(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'))

base_token = settings[config_network]['DOC']
secondary_token = settings[config_network]['RIF']
external_price_provider = '0x987ccC60c378a61d167B6DD1EEF7613c6f63938f'

price_provider = ExternalOraclePriceProviderFallback(network_manager)
tx_hash, tx_receipt = price_provider.constructor(external_price_provider, base_token, secondary_token)

price_provider_address = None
if tx_receipt:
    price_provider_address = tx_receipt.contractAddress
    print("Price provider deployed Contract Address: {address}".format(address=tx_receipt.contractAddress))
else:
    print("Error deploying price provider")

if price_provider_address:

    contract = DexPriceProviderChanger(network_manager)

    tx_hash, tx_receipt = contract.constructor(base_token,
                                               secondary_token,
                                               price_provider_address,
                                               execute_change=False)
    if tx_receipt:
        print("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))
    else:
        print("Error deploying changer")

"""

"""