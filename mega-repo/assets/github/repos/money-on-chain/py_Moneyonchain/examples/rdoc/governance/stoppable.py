from moneyonchain.networks import network_manager
from moneyonchain.governance import RDOCStopper
from moneyonchain.rdoc import RDOCMoC

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


contract_moc = RDOCMoC(network_manager).from_abi()
contract_stopper = RDOCStopper(network_manager).from_abi()

print("Paused: {0}".format(contract_moc.paused()))
print("Stoppable: {0}".format(contract_moc.stoppable()))
print("Stopper Address: {0}".format(contract_moc.stopper()))
print("Owner: {0}".format(contract_stopper.owner()))
print("MoC Address: {0}".format(contract_moc.address()))

# finally disconnect from network
network_manager.disconnect()
