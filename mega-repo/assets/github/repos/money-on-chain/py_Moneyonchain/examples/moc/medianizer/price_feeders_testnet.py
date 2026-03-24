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


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnet'

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


oracle_address = '0x78c892Dc5b7139d0Ec1eF513C9E28eDfAA44f2d4'
feeders = [('0x033c1D78Fbc34178A7Ee7fa64Fa6f31fEE8f79C2', '# MOC'),
           ('0x5d111d1b49Aa39d0172712266B0DE2F1eB9957F4', '# 2'),
           ('0x02baf7348859aAC6CfEEc53498A077790244bBe6', '# 3')]


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
