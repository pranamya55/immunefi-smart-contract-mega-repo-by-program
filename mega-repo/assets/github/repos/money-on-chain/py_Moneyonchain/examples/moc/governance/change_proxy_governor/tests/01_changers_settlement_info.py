from moneyonchain.networks import network_manager
from moneyonchain.moc import MoCSettlement

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger('default')

# Connect to network
network_manager.connect(connection_network='rskTestnetPublic', config_network='mocTestnet')

contract_moc = MoCSettlement(network_manager).from_abi()
log.info("Block Span: {0}".format(contract_moc.block_span()))
