from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoC

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()


connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


moc_sc = RDOCMoC(network_manager).from_abi()

account = '0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3'
info = moc_sc.reserve_allowance(account)
log.info("Reserve Allowance: {0}".format(info))

# finally disconnect from network
network_manager.disconnect()
