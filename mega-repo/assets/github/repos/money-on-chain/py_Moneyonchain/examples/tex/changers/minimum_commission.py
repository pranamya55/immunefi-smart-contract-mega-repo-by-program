"""
Minimum Commission changer
"""


from moneyonchain.networks import network_manager
from moneyonchain.tex import DexMinimumCommissionChanger

# Logging setup

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/minimum_commission.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network = 'rskMainnetPublic'
config_network = 'dexMainnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

contract = DexMinimumCommissionChanger(network_manager)

# New minimum commission to be set in USD.
minimum_commission = int(1.5 * 10 ** 18)

tx_receipt = contract.constructor(minimum_commission,
                                  execute_change=False)
if tx_receipt:
    print("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    print("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
