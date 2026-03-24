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


connection_network = 'rskTestnetPublic'
config_network = 'ethTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


oracle_address = '0x4D4254D3744e1E4beb090ab5d8eB48096ff4aE27'
feeders = [('0x4B3F85A1E85ef656E0EeF54d50Fb23Dc509332Cc', '# MOC 1 (DISABLED)'),
           ('0xEc2FA32050F5585dB4B15E60e1c21742b22740C4', '# MOC 2 <--OK'),
           ('0xF350BD966E62A7b4C58a34e3f10284435927Fb96', '# SOVRYN 1 (DISABLED)'),
           ('0x5C4B18226b84788760eB6627D82A70FD4c8c18D7', '# SOVRYN 2 (DISABLED)'),
           ('0x8Cc876f406D14aa4Ee051048eFc3C59307c61417', '# SOVRYN 3 <----OK'),
           ('0x58D462F575887a18dEbD0BB926845F997419cB27', '# SOVRYN TEST 2 <----OK')
           ]


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
