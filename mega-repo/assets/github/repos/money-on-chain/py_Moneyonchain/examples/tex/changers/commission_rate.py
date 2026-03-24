"""
Changer to change the commission rate in the MoC Decentralized Exchange
"""

from moneyonchain.networks import network_manager
from moneyonchain.tex import DexCommissionRateChanger

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/commission_rate.log',
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


contract = DexCommissionRateChanger(network_manager)

commission_rate = int(0.001 * 10 ** 18)

tx_receipt = contract.constructor(commission_rate,
                                  execute_change=False)
if tx_receipt:
    print("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    print("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
