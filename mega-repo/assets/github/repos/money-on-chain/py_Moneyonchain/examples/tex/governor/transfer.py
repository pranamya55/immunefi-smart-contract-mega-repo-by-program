"""
Transfer ownership governor control
"""

from moneyonchain.networks import NetworkManager
from moneyonchain.governance import DEXGovernor

import logging
import logging.config

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/insert_buy_limit_order.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network='rskTestnetPublic'
config_network = 'dexTestnet'

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


contract = DEXGovernor(network_manager).from_abi()

# New owner
new_owner = '0xC61820bFB8F87391d62Cd3976dDc1d35e0cf7128'

tx_hash, tx_receipt = contract.transfer_ownership(new_owner)

if tx_receipt:
    print("Successfully transfer ownership to : {new_owner}".format(new_owner=new_owner))
else:
    print("Error changing governance")

# finally disconnect from network
network_manager.disconnect()