"""
expirationPenaltyRate wad from 0 to 1 that represents the rate of the commission to charge when the order expire, 1 represents the full commission
"""

from moneyonchain.manager import ConnectionManager
from moneyonchain.changers import DexExpirationPenaltyRateChanger

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

contract = DexExpirationPenaltyRateChanger(connection_manager)

# expirationPenaltyRate wad from 0 to 1 that represents the rate of the commission to charge when the order expire,
# 1 represents the full commission
expiration_penalty_rate = int(0.2 * 10 ** 18)

tx_hash, tx_receipt = contract.constructor(expiration_penalty_rate,
                                           execute_change=False)
if tx_receipt:
    print("Changer Contract Address: {address}".format(address=tx_receipt.contractAddress))
else:
    print("Error deploying changer")

"""


"""