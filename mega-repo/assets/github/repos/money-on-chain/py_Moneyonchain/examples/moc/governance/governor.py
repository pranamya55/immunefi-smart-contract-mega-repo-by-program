from moneyonchain.networks import network_manager
from moneyonchain.governance import Governor

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger('default')

# Connect to network
network_manager.connect(connection_network='rskMainnetPublic', config_network='mocMainnet2')


governor = Governor(network_manager, contract_address='0x3B8853DF65AfbD94853E6d77ee0aB5590f41bB08').from_abi()

log.info("Owner: {0}".format(governor.owner()))

# finally disconnect from network
network_manager.disconnect()
