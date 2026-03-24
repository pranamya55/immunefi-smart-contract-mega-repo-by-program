"""
Price feeder verification. Test if pricefeeder is working and sending prices.
"""

from moneyonchain.networks import network_manager
from moneyonchain.medianizer import RDOCMoCMedianizer, \
    RDOCPriceFeed

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()


connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnet'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)


oracle_address = '0x9d4b2c05818A0086e641437fcb64ab6098c7BbEc'
feeders = [('0x462D7082F3671a3BE160638Be3f8C23Ca354F48A', '# MOC'),
           ('0xE0A3dce741b7EaD940204820B78E7990a136EAC1', '# RSK')]


oracle = RDOCMoCMedianizer(network_manager,
                           contract_address=oracle_address).from_abi()

print("Oracle price:")
print(oracle.peek())
print('')

for feed_c in feeders:
    feeder_cl = RDOCPriceFeed(network_manager,
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
