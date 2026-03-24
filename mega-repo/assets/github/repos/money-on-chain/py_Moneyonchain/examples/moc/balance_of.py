from moneyonchain.networks import network_manager
from web3 import Web3


connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)


user_address = '0x0a1Db9F51C1F06C5635Fde17711d94bF6159B5f7'

# Block Number
block_number = 4255498
balance = Web3.fromWei(network_manager.network_balance(user_address, block_identifier=block_number), 'ether')

print("RBTC Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))


# Block Number
block_number = 4255499
balance = Web3.fromWei(network_manager.network_balance(user_address, block_identifier=block_number), 'ether')

print("RBTC Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

# finally disconnect from network
network_manager.disconnect()
