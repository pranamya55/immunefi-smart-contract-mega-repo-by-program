"""
Price feeder verification. Test if pricefeeder is working and sending prices.
"""
import datetime
from tabulate import tabulate

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

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)


oracle_address = '0x504EfCadFB020d6bBaeC8a5c5BB21453719d0E00'
feeders = [('0x461750b4824b14c3d9b7702bC6fBB82469082b23', '# MOC'),
           ('0xBEd51D83CC4676660e3fc3819dfAD8238549B975', '# RSK')]

oracle = RDOCMoCMedianizer(network_manager,
                           contract_address=oracle_address).from_abi()

feeder_moc = RDOCPriceFeed(network_manager,
                           contract_address=feeders[0][0],
                           contract_address_moc_medianizer=oracle_address).from_abi()

feeder_rsk = RDOCPriceFeed(network_manager,
                           contract_address=feeders[1][0],
                           contract_address_moc_medianizer=oracle_address).from_abi()

range_blocks = [5285880, 5285888]
block_skip = 3

display_table = []
titles = ['blockNumber', 'Price Oracle', 'Price Feeder MOC', 'Price Feeder ROC', 'Timestamp']

for block_n in range(range_blocks[0], range_blocks[1], block_skip):

    print("Indexing Block {0} / {1}".format(block_n, range_blocks[1]))

    ts = network_manager.block_timestamp(block_n)
    dt = ts - datetime.timedelta(hours=0)
    d_timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")

    display_table.append([
        block_n,
        oracle.peek(block_identifier=block_n)[0],
        feeder_moc.peek(block_identifier=block_n)[0],
        feeder_rsk.peek(block_identifier=block_n)[0],
        d_timestamp])

print(tabulate(display_table, headers=titles, tablefmt="pipe"))

# finally disconnect from network
network_manager.disconnect()
