"""
Price Provider Changer
"""

from moneyonchain.manager import ConnectionManager
from moneyonchain.changers import DexPriceProviderChanger
from moneyonchain.dex import MocBproBtcPriceProviderFallback

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


WRBTC / BPRO

"""

base_token = '0x09b6ca5E4496238A1F176aEa6Bb607DB96c2286E'
secondary_token = '0x4dA7997A819bb46B6758B9102234c289dD2Ad3bf'
moc_state = '0x0adb40132cB0ffcEf6ED81c26A1881e214100555'


price_provider = MocBproBtcPriceProviderFallback(connection_manager)
tx_hash, tx_receipt = price_provider.constructor(moc_state, base_token, secondary_token)

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
Connecting to dexTestnet...
Connected: True
2020-10-15 15:48:20 root         INFO     Deploying new contract...
2020-10-15 15:48:58 root         INFO     Deployed contract done!
2020-10-15 15:48:58 root         INFO     0x446a320b076a9733410500a6b1c51a4fb87e273bcdf011d54fabed5777605e12
2020-10-15 15:48:58 root         INFO     AttributeDict({'transactionHash': HexBytes('0x446a320b076a9733410500a6b1c51a4fb87e273bcdf011d54fabed5777605e12'), 'transactionIndex': 10, 'blockHash': HexBytes('0xc32eef2b1ea04d0afa25e0059a74a165bee44cf734de658edb2c7e7b0f1e3cc1'), 'blockNumber': 1259850, 'cumulativeGasUsed': 996821, 'gasUsed': 403716, 'contractAddress': '0x76C48Ed95418B73cdA7051AB99Bf0aa89e4e6cee', 'logs': [], 'from': '0xA8342cC05241E0d940E1c74043faCd931562f19a', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-10-15 15:48:58 root         INFO     Contract Address: 0x76C48Ed95418B73cdA7051AB99Bf0aa89e4e6cee
2020-10-15 15:48:58 root         INFO     Deploying new contract...
Price provider deployed Contract Address: 0x76C48Ed95418B73cdA7051AB99Bf0aa89e4e6cee
2020-10-15 15:49:24 root         INFO     Deployed contract done!
2020-10-15 15:49:24 root         INFO     0x55fee3ba0f40f58dfb9afb50e7a41aea66e002cec7a880263f21cf5e34cf9e35
2020-10-15 15:49:24 root         INFO     AttributeDict({'transactionHash': HexBytes('0x55fee3ba0f40f58dfb9afb50e7a41aea66e002cec7a880263f21cf5e34cf9e35'), 'transactionIndex': 10, 'blockHash': HexBytes('0xa48683d1602965c11beefb768a2ce34825571214e57875ee43da1e6aed1e8b9d'), 'blockNumber': 1259851, 'cumulativeGasUsed': 1045881, 'gasUsed': 264222, 'contractAddress': '0xcC182ee62DC88eE55746D37da5e636aD887F714F', 'logs': [], 'from': '0xA8342cC05241E0d940E1c74043faCd931562f19a', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-10-15 15:49:24 root         INFO     Changer Contract Address: 0xcC182ee62DC88eE55746D37da5e636aD887F714F
Changer Contract Address: 0xcC182ee62DC88eE55746D37da5e636aD887F714F
"""