"""
Price Provider Changer
"""

from moneyonchain.manager import ConnectionManager
from moneyonchain.changers import DexPriceProviderChanger
from moneyonchain.dex import MocRiskProReservePriceProviderFallback

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

RIF/RIFP

"""

base_token = '0x19F64674D8A5B4E652319F5e239eFd3bc969A1fE'
secondary_token = '0x23A1aA7b11e68beBE560a36beC04D1f79357f28d'
moc_state = '0x496eD67F77D044C8d9471fe86085Ccb5DC4d2f63'


price_provider = MocRiskProReservePriceProviderFallback(connection_manager)
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
2020-10-15 16:54:44 root         INFO     Deploying new contract...
Price provider deployed Contract Address: 0x83aF00e2ad1970A5d27660e7bf2223f1eDF3d080
2020-10-15 16:55:26 root         INFO     Deployed contract done!
2020-10-15 16:55:26 root         INFO     0xc8585117f2f3c5a198cedea0636818453bacfe8d78a91a1fd7be6260b95c5dca
2020-10-15 16:55:26 root         INFO     AttributeDict({'transactionHash': HexBytes('0xc8585117f2f3c5a198cedea0636818453bacfe8d78a91a1fd7be6260b95c5dca'), 'transactionIndex': 8, 'blockHash': HexBytes('0x01fb79fe8186502749226270447d5683aafb401b408104a742a6d84bca0c5947'), 'blockNumber': 1259978, 'cumulativeGasUsed': 667676, 'gasUsed': 403716, 'contractAddress': '0x83aF00e2ad1970A5d27660e7bf2223f1eDF3d080', 'logs': [], 'from': '0xA8342cC05241E0d940E1c74043faCd931562f19a', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-10-15 16:55:26 root         INFO     Contract Address: 0x83aF00e2ad1970A5d27660e7bf2223f1eDF3d080
2020-10-15 16:55:26 root         INFO     Deploying new contract...
Changer Contract Address: 0x53fDb0F6f11cbEb0876e3B123F974B4b384a216A
2020-10-15 16:56:31 root         INFO     Deployed contract done!
2020-10-15 16:56:31 root         INFO     0x4dac727c23c174ca12b2dc8ef00626260dfc41aac49d28519cbfe203d5fd11a4
2020-10-15 16:56:31 root         INFO     AttributeDict({'transactionHash': HexBytes('0x4dac727c23c174ca12b2dc8ef00626260dfc41aac49d28519cbfe203d5fd11a4'), 'transactionIndex': 9, 'blockHash': HexBytes('0x298b57019fbc6ae665d28a9b1e54e9687acc3f343391b394e2d77ddc29fd1482'), 'blockNumber': 1259980, 'cumulativeGasUsed': 585795, 'gasUsed': 264158, 'contractAddress': '0x53fDb0F6f11cbEb0876e3B123F974B4b384a216A', 'logs': [], 'from': '0xA8342cC05241E0d940E1c74043faCd931562f19a', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-10-15 16:56:31 root         INFO     Changer Contract Address: 0x53fDb0F6f11cbEb0876e3B123F974B4b384a216A
"""