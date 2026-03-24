
from moneyonchain.networks import network_manager
from moneyonchain.governance import Governor

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


batch_changer = '0x0cbCD4E3a5F7E159F4b21530e967cFC83DB8Ab8E'


log.info("Executing change....")
governor = Governor(network_manager).from_abi()
tx_args = governor.tx_arguments()
tx_receipt = governor.execute_change(batch_changer)
log.info("Change successfull!")


# finally disconnect from network
network_manager.disconnect()
