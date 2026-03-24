from moneyonchain.networks import network_manager
from moneyonchain.moc import MoCSettlement

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/fix_task_pointer.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network = 'bscTestnet'
config_network = 'bnbAlphaTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

settlement = MoCSettlement(network_manager).from_abi()

tx_args = settlement.tx_arguments()
tx_receipt = settlement.sc.fixTasksPointer(tx_args)

# finally disconnect from network
network_manager.disconnect()
