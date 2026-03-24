from web3 import Web3
from moneyonchain.networks import network_manager
from moneyonchain.tokens import RIF

connection_network = 'rskMainnetPublic'
config_network = 'rdocMainnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


rif_token = RIF(network_manager).from_abi()

account_address = '0xc61820BFb8F87391d62cD3976DDC1D35E0cF7128'

block_number = 2405000

# balance_on_block = Web3.fromWei(
#     network_manager.balance_block_number(account_address, block_number), 'ether')
# print("Balance: [{0}] on block: [{1}] Balance: [{2}] RBTC".format(
#     account_address,
#     block_number,
#     balance_on_block))

balance_on_block = rif_token.balance_of(account_address, block_identifier=block_number)
print("Balance: [{0}] on block: [{1}] Balance: [{2}] RIF".format(
    account_address,
    block_number,
    balance_on_block))


block_number = 2467288

# balance_on_block = Web3.fromWei(
#     network_manager.balance_block_number(account_address, block_number), 'ether')
# print("Balance: [{0}] on block: [{1}] Balance: [{2}] RBTC".format(
#     account_address,
#     block_number,
#     balance_on_block))

balance_on_block = rif_token.balance_of(account_address, block_identifier=block_number)
print("Balance: [{0}] on block: [{1}] Balance: [{2}] RIF".format(
    account_address,
    block_number,
    balance_on_block))

# finally disconnect from network
network_manager.disconnect()
