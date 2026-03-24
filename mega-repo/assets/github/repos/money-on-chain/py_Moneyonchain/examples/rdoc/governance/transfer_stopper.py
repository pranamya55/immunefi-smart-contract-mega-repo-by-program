"""
Transfer ownership stopper control
"""

from moneyonchain.networks import network_manager
from moneyonchain.governance import RDOCStopper

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/transfer.log',
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

contract = RDOCStopper(network_manager).from_abi()

# New owner
if config_network in ['rdocTestnetAlpha', 'rdocTestnet']:
    new_owner = '0xf69287F5Ca3cC3C6d3981f2412109110cB8af076'
else:
    new_owner = '0xC61820bFB8F87391d62Cd3976dDc1d35e0cf7128'


new_owner = '0xC61820bFB8F87391d62Cd3976dDc1d35e0cf7128'
tx_receipt = contract.transfer_ownership(new_owner)

if tx_receipt:
    log.info("Successfully transfer ownership to : {new_owner}".format(new_owner=new_owner))
else:
    log.info("Error changing governance")

# finally disconnect from network
network_manager.disconnect()
