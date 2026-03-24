from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoCInrate, RDOCMoC

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()


connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnetAlpha'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_inrate = RDOCMoCInrate(network_manager).from_abi()

print("Bitpro rate: {0}".format(moc_inrate.bitpro_rate()))
print("Bitpro interest blockspan: {0}".format(moc_inrate.bitpro_interest_blockspan()))
print("Commission rate: {0}".format(moc_inrate.commision_rate()))
print("last_bitpro_interest_block: {0}".format(moc_inrate.last_bitpro_interest_block()))
print("daily_enabled: {0}".format(moc_inrate.daily_enabled()))
print("daily_inrate: {0}".format(moc_inrate.daily_inrate()))
print("spot_inrate: {0}".format(moc_inrate.spot_inrate()))
print("commission_address: {0}".format(moc_inrate.commission_address()))
print("last_daily_pay: {0}".format(moc_inrate.last_daily_pay()))
print("bitpro_interest_address: {0}".format(moc_inrate.bitpro_interest_address()))
print("is_bitpro_interest_enabled: {0}".format(moc_inrate.is_bitpro_interest_enabled()))

# finally disconnect from network
network_manager.disconnect()