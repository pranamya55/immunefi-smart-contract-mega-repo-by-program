"""
Changer to change the max blocks for ticks in the MoC Decentralized Exchange
"""

from moneyonchain.manager import ConnectionManager
from moneyonchain.changers import DexMaxBlocksForTickChanger

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

contract = DexMaxBlocksForTickChanger(connection_manager)

max_blocks_for_ticks = 20

tx_hash, tx_receipt = contract.constructor(max_blocks_for_ticks,
                                           execute_change=False)
if tx_receipt:
    print("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))
else:
    print("Error deploying changer")

"""


"""