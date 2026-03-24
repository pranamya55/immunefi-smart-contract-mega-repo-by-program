import datetime
from tabulate import tabulate

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoCVendors

from web3 import Web3

connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_vendors = MoCVendors(network_manager).from_abi()
vendor_account = '0xC61820bFB8F87391d62Cd3976dDc1d35e0cf7128'
range_blocks = [4672793, 5212793]
block_skip = 2880
hours_delta = 0

display_table = []
titles = ['blockNumber', 'Date', 'Total Paid in Moc']

for block_n in range(range_blocks[0], range_blocks[1], block_skip):

    print("Indexing block {0} / {1}".format(block_n, range_blocks[1]))

    ts = network_manager.block_timestamp(block_n)
    dt = ts - datetime.timedelta(hours=hours_delta)
    d_timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")

    total_paid = moc_vendors.total_paid_in_moc(vendor_account, block_identifier=block_n)
    display_table.append([block_n, d_timestamp, total_paid])

print(tabulate(display_table, headers=titles, tablefmt="pipe"))

# finally disconnect from network
network_manager.disconnect()
