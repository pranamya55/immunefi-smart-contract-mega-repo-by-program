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


connection_network = 'rskMainnetPublic'
config_network = 'rdocMainnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


oracle_address = '0x504EfCadFB020d6bBaeC8a5c5BB21453719d0E00'
feeders = [('0x4B6a4151D59b30a09C3565c17d83176cfAea6474', '#1 <-'),
           ('0x461750b4824b14c3d9b7702bC6fBB82469082b23', '#2'),
           ('0x94446fA55c7740Df3494804424734721B3Ea0354', '#3 <-'),
           ('0xBEd51D83CC4676660e3fc3819dfAD8238549B975', '#4')]

# oracle_address = '0x9d4b2c05818A0086e641437fcb64ab6098c7BbEc'
# feeders = [('0x462D7082F3671a3BE160638Be3f8C23Ca354F48A', '#1'),
#            ('0xE0A3dce741b7EaD940204820B78E7990a136EAC1', '#2'),
#            ('0xFFF8e36C9e9660a88CD16A215338190AaDbB4F50', '#3')]


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
        print(oracle.indexes(feed_c[0]))
    else:
        print('Enabled: False')

    print('')

# finally disconnect from network
network_manager.disconnect()
