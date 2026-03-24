"""
Price Provider Changer
"""

from moneyonchain.manager import ConnectionManager
from moneyonchain.changers import DexPriceProviderChanger
from moneyonchain.dex import MocRiskProUsdPriceProviderFallback

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

RDOC/RIFP

"""

base_token = '0xC3De9F38581f83e281f260d0DdbaAc0e102ff9F8'
secondary_token = '0x23A1aA7b11e68beBE560a36beC04D1f79357f28d'
moc_state = '0x496eD67F77D044C8d9471fe86085Ccb5DC4d2f63'


price_provider = MocRiskProUsdPriceProviderFallback(connection_manager)
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
2020-10-15 16:51:06 root         INFO     Deploying new contract...
Connected: True
2020-10-15 16:51:41 root         INFO     Deployed contract done!
2020-10-15 16:51:41 root         INFO     0x9208eec02c28894391c332d4e2a82fb2a60692e306cfe681757c88f408c67193
2020-10-15 16:51:41 root         INFO     AttributeDict({'transactionHash': HexBytes('0x9208eec02c28894391c332d4e2a82fb2a60692e306cfe681757c88f408c67193'), 'transactionIndex': 11, 'blockHash': HexBytes('0x30ada84aa0f44a69a43b1d24aacf4ee6025bf70945b889e6c029a21c0ddb0c99'), 'blockNumber': 1259973, 'cumulativeGasUsed': 2197134, 'gasUsed': 403716, 'contractAddress': '0xBE9d90405fdf72Dc1f636Da0de98a05c0fB6d674', 'logs': [], 'from': '0xA8342cC05241E0d940E1c74043faCd931562f19a', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-10-15 16:51:41 root         INFO     Contract Address: 0xBE9d90405fdf72Dc1f636Da0de98a05c0fB6d674
2020-10-15 16:51:41 root         INFO     Deploying new contract...
Price provider deployed Contract Address: 0xBE9d90405fdf72Dc1f636Da0de98a05c0fB6d674
Changer Contract Address: 0xa52a9C637C1DFf95C158ecA1A3131909fBa5448D
2020-10-15 16:52:34 root         INFO     Deployed contract done!
2020-10-15 16:52:34 root         INFO     0x41b7cc027b89fa1e825907b7d4dd1a60988f72fcab3d9f9a406bf1328e1b4618
2020-10-15 16:52:34 root         INFO     AttributeDict({'transactionHash': HexBytes('0x41b7cc027b89fa1e825907b7d4dd1a60988f72fcab3d9f9a406bf1328e1b4618'), 'transactionIndex': 7, 'blockHash': HexBytes('0x46718eba3e355d1359ab84dbe7f9e4273437fa0b1ba9b410c83089feab73ccb3'), 'blockNumber': 1259974, 'cumulativeGasUsed': 518717, 'gasUsed': 264222, 'contractAddress': '0xa52a9C637C1DFf95C158ecA1A3131909fBa5448D', 'logs': [], 'from': '0xA8342cC05241E0d940E1c74043faCd931562f19a', 'to': None, 'root': '0x01', 'status': 1, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')})
2020-10-15 16:52:34 root         INFO     Changer Contract Address: 0xa52a9C637C1DFf95C158ecA1A3131909fBa5448D
"""