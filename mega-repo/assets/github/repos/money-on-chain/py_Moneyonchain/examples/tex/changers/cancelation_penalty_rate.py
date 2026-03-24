"""
Changer to change the cancelation penalty rate used in the MoC Decentralized Exchange
cancelationPenaltyRate wad from 0 to 1 that represents the rate of the commission to charge as cancelation penalty, 1 represents the full commission
"""

from moneyonchain.networks import network_manager
from moneyonchain.tex import DexCancelationPenaltyRateChanger

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/changers_cancelation_penalty_rate.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)

connection_network = 'rskTestnetPublic'
config_network = 'dexTestnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


contract = DexCancelationPenaltyRateChanger(network_manager)

# New cancelation penalty rate to be set. Must be between 0 and 1(RATE_PRECISION)
cancelation_penalty_rate = int(0 * 10 ** 18)

tx_receipt = contract.constructor(cancelation_penalty_rate,
                                  execute_change=False)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
