"""
Price Provider Changer
"""

from moneyonchain.manager import ConnectionManager
from moneyonchain.changers import DexPriceProviderChanger
from moneyonchain.dex import UnityPriceProvider

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger('default')

network = 'dexTestnet'
connection_manager = ConnectionManager(network=network)
print("Connecting to %s..." % network)
print("Connected: {conectado}".format(conectado=connection_manager.is_connected))

"""


DOC / RDOC

"""

base_token = '0xCB46c0ddc60D18eFEB0E586C17Af6ea36452Dae0'
secondary_token = '0xC3De9F38581f83e281f260d0DdbaAc0e102ff9F8'


price_provider = UnityPriceProvider(connection_manager)
tx_hash, tx_receipt = price_provider.constructor()

price_provider_address = None
if tx_receipt:
    price_provider_address = tx_receipt.contractAddress
    print("Price provider deployed Contract Address: {address}".format(address=tx_receipt.contractAddress))
else:
    print("Error deploying price provider")

if price_provider_address:

    contract = DexPriceProviderChanger(connection_manager)

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