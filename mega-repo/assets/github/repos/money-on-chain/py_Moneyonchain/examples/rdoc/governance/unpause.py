"""

This unpause MOC Contract

"""

from moneyonchain.networks import network_manager
from moneyonchain.governance import RDOCStopper
from moneyonchain.rdoc import RDOCMoC

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/unpause.log',
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
config_network = 'rdocMainnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


contract_moc = RDOCMoC(network_manager).from_abi()
contract_stopper = RDOCStopper(network_manager).from_abi()

contract_to_pause = contract_moc.address()
tx_receipt = contract_stopper.unpause(contract_to_pause)
if tx_receipt:
    log.info("Stop Contract Address: {address} successfully!".format(address=contract_to_pause))
else:
    log.info("Error Stopping contract")


# finally disconnect from network
network_manager.disconnect()
