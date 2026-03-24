from moneyonchain.networks import NetworkManager
from moneyonchain.governance import MoCStopper
from moneyonchain.moc import MoC

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger('default')


connection_network='rskMainnetPublic'
config_network = 'mocMainnet2'

log.info('Connecting enviroment {0}...'.format(config_network))

# init network manager
# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager = NetworkManager(
    connection_network=connection_network,
    config_network=config_network)

# run install() if is the first time and you want to install
# networks connection from brownie
# network_manager.install()

# Connect to network
network_manager.connect()


contract_moc = MoC(network_manager).from_abi()
contract_stopper = MoCStopper(network_manager).from_abi()

log.info("MoC Contract: {0}".format(contract_moc.address()))
log.info("Paused: {0}".format(contract_moc.paused()))
log.info("Stoppable: {0}".format(contract_moc.stoppable()))
log.info("Stopper: {0}".format(contract_moc.stopper()))
log.info("Owner: {0}".format(contract_stopper.owner()))

# finally disconnect from network
network_manager.disconnect()
