"""
Price feeder verification. Test if pricefeeder is working and sending prices.
"""

from moneyonchain.networks import network_manager
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

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


oracle_address = '0x7B19bb8e6c5188eC483b784d6fB5d807a77b21bF'
feeder_address_1 = '0xfE05Ee3d651670F807Db7dD56e1E0FCBa29B234a'
feeder_address_2 = '0xE94007E81412eDfdB87680F768e331E8c691f0e1'

oracle = MoCMedianizer(network_manager,
                       contract_address=oracle_address).from_abi()

feeder_1 = PriceFeed(network_manager,
                     contract_address=feeder_address_1,
                     contract_address_moc_medianizer=oracle_address).from_abi()

log.info("Oracle price:")
log.info(oracle.peek())

log.info("Price Feeder 1")
log.info("===============")

log.info("Price feeder price and have value (if have value if false, no price setted) :")
log.info(feeder_1.peek())

log.info("Index > 0 is active price feeder")
log.info(oracle.indexes(feeder_address_1))

feeder_2 = PriceFeed(network_manager,
                     contract_address=feeder_address_2,
                     contract_address_moc_medianizer=oracle_address).from_abi()


log.info("Price Feeder 2")
log.info("===============")

log.info("Price feeder price and have value (if have value if false, no price setted) :")
log.info(feeder_2.peek())

log.info("Index > 0 is active price feeder")
log.info(oracle.indexes(feeder_address_2))

# finally disconnect from network
network_manager.disconnect()
