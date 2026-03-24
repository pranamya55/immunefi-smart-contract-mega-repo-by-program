"""
Price feeder verification. Test if pricefeeder is working and sending prices.
"""

from moneyonchain.networks import network_manager
from moneyonchain.medianizer import USDTMoCMedianizer, \
    USDTPriceFeed

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()


connection_network = 'rskMainnetPublic'
config_network = 'tetherMainnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


oracle_address = '0x5741d55C96176eEca86316b5840Cb208784d5188'
feeders = [('0xda6BA2D0162f1C5f3E1F5722E527DB53bA24aD31', '# MOC 1'),
           ('0x1f6a8F851A661c04C09A6E7dDdc759aa48cf2FfC', '# TROPYKUS 1'),
           ('0xdADF68aFf1981B605101473cC996581A5B17Fc68', '# RSK 1')]


oracle = USDTMoCMedianizer(network_manager,
                           contract_address=oracle_address).from_abi()

print("Oracle price:")
print(oracle.peek())
print('')

for feed_c in feeders:
    feeder_cl = USDTPriceFeed(network_manager,
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
