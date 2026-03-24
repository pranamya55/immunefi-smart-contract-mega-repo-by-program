"""
Price feeder verification. Test if pricefeeder is working and sending prices.
"""

from moneyonchain.networks import network_manager
from moneyonchain.medianizer import ETHMoCMedianizer, \
    ETHPriceFeed

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()


connection_network = 'rskMainnetPublic'
config_network = 'ethMainnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


oracle_address = '0x68862C30d45605EAd8D01eF1632F7BFB18FAB587'
feeders = [('0x87079F2669192626Ca572A1264f11DAF2d40AA84', '# MOC 1 (DISABLED)'),
           ('0xe76Bd65f9C5fD95b6120532CE6a254FA0fB62208', '# MOC 2 <-- OK'),
           ('0x85c6cD0BCce63fdF9D3fA4C0661aEEd0976C9B97', '# SOVRYN 1 (DISABLED)'),
           ('0xD4b0244F06B4482248Fc1388b4AC73de3308eb2a', '# SOVRYN 2 <-- OK')]


oracle = ETHMoCMedianizer(network_manager,
                          contract_address=oracle_address).from_abi()

print("Oracle price:")
print(oracle.peek())
print('')

for feed_c in feeders:
    feeder_cl = ETHPriceFeed(network_manager,
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
