from moneyonchain.networks import network_manager
from moneyonchain.moc_vendors import MoCStateLiquidationEnabledChanger

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/changers_liquidation_enabled.log',
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
config_network = 'mocTestnetAlpha3'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


contract = MoCStateLiquidationEnabledChanger(network_manager)
is_enabled = False

tx_receipt = contract.constructor(is_enabled, execute_change=True)
if tx_receipt:
    print("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    print("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
