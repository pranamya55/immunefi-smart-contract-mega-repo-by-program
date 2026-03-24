from moneyonchain.networks import network_manager
from moneyonchain.moc import MoC

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
log.info("Implementation: {0}".format(contract_moc.implementation()))
log.info("Max riskpro: {0}".format(contract_moc.max_mint_riskpro_available()))



# finally disconnect from network
network_manager.disconnect()
