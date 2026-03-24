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


connection_network = 'rskTestnetPublic'
config_network = 'tetherTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


oracle_address = '0xB4A44672b55d66fAFA23b4F9Ba28c9C55F76fbfB'
feeders = [
    ('0x15c7cF2c90695176dadB6c19bE34a2588Bd4eA53', '# MOC 1'),
    ('0x6E2A377da524B2a6b5c86472b1c1906cC0f58B22', '# TROPYKUS 1'),
    ('0x157D53a2ecB44D190E5199670cd34C5c513b72Ec', '# RSK 1'),
    ('0xD942e57ECc9C016025ee30CE4acF302379Da215C', '# RSK 2')
]


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
