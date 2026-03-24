import datetime
from tabulate import tabulate

from moneyonchain.networks import network_manager
from moneyonchain.tokens import BProToken, MoCToken
from web3 import Web3

connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

bpro_token = BProToken(network_manager).from_abi()
moc_token = MoCToken(network_manager).from_abi()

user_address = '0x199581b423d9707b4b49921CE740c4e4856F0Da9'
list_block_numbers = [3817816, 3817817]

display_table = []
titles = ['blockNumber', 'Account', 'MoC Balance', 'BPro Balance']

for block_n in list_block_numbers:
    bpro_balance = bpro_token.balance_of(user_address, block_identifier=block_n)
    moc_balance = moc_token.balance_of(user_address, block_identifier=block_n)
    display_table.append([block_n, user_address, moc_balance, bpro_balance])

print(tabulate(display_table, headers=titles, tablefmt="pipe"))

# finally disconnect from network
network_manager.disconnect()
