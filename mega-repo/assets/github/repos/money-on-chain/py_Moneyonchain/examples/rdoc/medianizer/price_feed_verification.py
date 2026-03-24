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
feeder_address_1 = '0x461750b4824b14c3d9b7702bC6fBB82469082b23'
feeder_address_2 = '0xBEd51D83CC4676660e3fc3819dfAD8238549B975'

oracle = RDOCMoCMedianizer(network_manager,
                           contract_address=oracle_address).from_abi()

feeder_1 = RDOCPriceFeed(network_manager,
                         contract_address=feeder_address_1,
                         contract_address_moc_medianizer=oracle_address).from_abi()

print("Oracle price:")
print(oracle.peek())

print("Price Feeder 1")
print("===============")

print("Price feeder price and have value (if have value if false, no price setted) :")
print(feeder_1.peek())

print("Index > 0 is active price feeder")
print(oracle.indexes(feeder_address_1))


feeder_2 = RDOCPriceFeed(network_manager,
                         contract_address=feeder_address_2,
                         contract_address_moc_medianizer=oracle_address).from_abi()

print("Price Feeder 2")
print("===============")

print("Price feeder price and have value (if have value if false, no price setted) :")
print(feeder_2.peek())

print("Index > 0 is active price feeder")
print(oracle.indexes(feeder_address_2))

# finally disconnect from network
network_manager.disconnect()
