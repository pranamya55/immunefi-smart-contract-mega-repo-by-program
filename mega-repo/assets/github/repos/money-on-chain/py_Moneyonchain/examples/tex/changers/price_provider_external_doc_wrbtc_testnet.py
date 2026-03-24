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
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/price_provider_external_doc_wrbtc.log',
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

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


# load settings from file
settings = options_from_settings(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'))

base_token = settings[config_network]['DOC']
secondary_token = settings[config_network]['WRBTC']
external_price_provider = '0xbffBD993FF1d229B0FfE55668F2009d20d4F7C5f'

price_provider = ExternalOraclePriceProviderFallback(network_manager)
tx_receipt = price_provider.constructor(external_price_provider, base_token, secondary_token)

price_provider_address = None
if tx_receipt:
    price_provider_address = tx_receipt.contract_address
    log.info("Price provider deployed Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying price provider")

if price_provider_address:

    contract = DexPriceProviderChanger(network_manager)

    tx_receipt = contract.constructor(base_token,
                                      secondary_token,
                                      price_provider_address,
                                      execute_change=False)
    if tx_receipt:
        log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
    else:
        log.info("Error deploying changer")

"""

"""