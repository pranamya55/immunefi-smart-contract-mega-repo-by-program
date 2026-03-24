"""

This pause MOC Contract

"""

from moneyonchain.networks import NetworkManager
from moneyonchain.governance import MoCStopper
from moneyonchain.moc import MoC

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/pause.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


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

contract_to_pause = contract_moc.address()
tx_receipt = contract_stopper.pause(contract_to_pause)
if tx_receipt:
    log.info("Stop Contract Address: {address} successfully!".format(address=contract_to_pause))
else:
    log.info("Error Stopping contract")

# finally disconnect from network
network_manager.disconnect()
