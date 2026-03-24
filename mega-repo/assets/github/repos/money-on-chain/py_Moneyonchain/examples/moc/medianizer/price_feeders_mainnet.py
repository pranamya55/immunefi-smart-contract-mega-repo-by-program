"""
Price feeder verification. Test if pricefeeder is working and sending prices.
"""

from moneyonchain.networks import NetworkManager
from moneyonchain.medianizer import MoCMedianizer, \
    PriceFeed


import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()


connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'

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


oracle_address = '0x7B19bb8e6c5188eC483b784d6fB5d807a77b21bF'
feeders = [('0xfE05Ee3d651670F807Db7dD56e1E0FCBa29B234a', '# MOC'),
           ('0xE94007E81412eDfdB87680F768e331E8c691f0e1', '# RSK')]


oracle = MoCMedianizer(network_manager,
                       contract_address=oracle_address).from_abi()

print("Oracle price:")
print(oracle.peek())
print('')

for feed_c in feeders:
    feeder_cl = PriceFeed(network_manager,
                          contract_address=feed_c[0],
                          contract_address_moc_medianizer=oracle_address).from_abi()

    print("Price Feeder: {0}".format(feed_c[1]))
    print("===============")
    print('Address: {0}'.format(feed_c[0]))
    print('Price: {0}'.format(feeder_cl.peek()))
    if int(oracle.indexes(feed_c[0])) > 0:
        print('Enabled: True')
    else:
        print('Enabled: False')
    print('')

# finally disconnect from network
network_manager.disconnect()
