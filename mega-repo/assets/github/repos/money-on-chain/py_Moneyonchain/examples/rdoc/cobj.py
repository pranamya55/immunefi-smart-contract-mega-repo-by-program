from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoCState

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()


connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnetAlpha'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_state = RDOCMoCState(network_manager).from_abi()

info = moc_state.cobj()
log.info("CObj: {0}".format(info))

info = moc_state.cobj_X2()
log.info("CObj X2: {0}".format(info))

info = moc_state.global_coverage()
log.info("Global Coverage: {0}".format(info))

# finally disconnect from network
network_manager.disconnect()