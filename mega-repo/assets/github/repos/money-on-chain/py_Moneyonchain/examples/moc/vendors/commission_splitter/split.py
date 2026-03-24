from moneyonchain.networks import network_manager
from moneyonchain.moc_vendors import VENDORSMoCInrate, VENDORSCommissionSplitter

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/split.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


# Connect to network
network_manager.connect(connection_network='rskTestnetPublic', config_network='mocTestnetAlpha')

splitter = VENDORSCommissionSplitter(network_manager).from_abi()

tx_receipt = splitter.split()
if tx_receipt:
    log.info("Sucessfully splited!")
else:
    log.info("Error splited!!!")

# finally disconnect from network
network_manager.disconnect()
