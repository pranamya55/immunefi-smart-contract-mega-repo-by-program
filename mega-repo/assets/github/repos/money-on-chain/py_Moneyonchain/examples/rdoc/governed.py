from moneyonchain.networks import network_manager
from moneyonchain.governance import RDOCGoverned

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger('default')


connection_network = 'rskMainnetPublic'
config_network = 'rdocMainnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


contact_address = network_manager.options['networks'][config_network]['addresses']['CommissionSplitter']
contract = RDOCGoverned(network_manager, contract_address=contact_address).from_abi()
print(contract.governor())

governor_address = network_manager.options['networks'][config_network]['addresses']['governor']
tx_receipt = contract.initialize(governor_address)
if tx_receipt:
    print("Sucessfully initialized")
else:
    print("Error initialized")


# finally disconnect from network
network_manager.disconnect()
