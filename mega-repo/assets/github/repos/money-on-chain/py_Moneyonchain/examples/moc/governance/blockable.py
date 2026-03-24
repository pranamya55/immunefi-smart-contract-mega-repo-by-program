from moneyonchain.networks import network_manager
from moneyonchain.moc import MoC
from moneyonchain.governance import BlockableGovernor

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger('default')

# Connect to network
network_manager.connect(connection_network='rskTestnetPublic', config_network='mocTestnet')


contract_moc = MoC(network_manager).from_abi()
log.info("Governor: {0}".format(contract_moc.governor()))

governor = BlockableGovernor(network_manager).from_abi()


log.info("Is Blocked: {0}".format(governor.is_blocked()))
log.info("Block Until: {0}".format(governor.unblock_date()))

# finally disconnect from network
network_manager.disconnect()
