from moneyonchain.networks import network_manager
from moneyonchain.tokens import BProToken
from web3 import Web3

connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


bpro_token = BProToken(network_manager).from_abi()

user_address = '0x5d2691B2F9f4F89e5d6a6759079dF629B36CCF51'
moc_address = '0xf773B590AF754D597770937fa8eA7ABDf2668370'

# Block Number
block_number = 2609806
print("BLOCK NUMBER: {0}".format(block_number))
print("--------------------")

# RBTC user address
balance = Web3.fromWei(network_manager.balance_block_number(user_address, block_number=block_number), 'ether')
print("RBTC Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

# BPRO user address
balance = bpro_token.balance_of(user_address, block_identifier=block_number)
print("BPRO Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

# SC moc address
balance = Web3.fromWei(network_manager.balance_block_number(moc_address, block_number=block_number), 'ether')
print("RBTC Balance of (MOC Contract): {0} balance: {1} blockNumber: {2}".format(
    moc_address,
    balance,
    block_number))

# SC BPRO CONTRACT
balance = bpro_token.total_supply(block_identifier=block_number)
print("BPRO Balance of (BPRO Contract): {0} balance: {1} blockNumber: {2}".format(
    bpro_token.address(),
    balance,
    block_number))


# Block Number
block_number = 2609807
print("")
print("BLOCK NUMBER: {0}".format(block_number))
print("--------------------")

balance = Web3.fromWei(network_manager.balance_block_number(user_address, block_number=block_number), 'ether')
print("RBTC Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

# BPRO user address
balance = bpro_token.balance_of(user_address, block_identifier=block_number)
print("BPRO Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

balance = Web3.fromWei(network_manager.balance_block_number(moc_address, block_number=block_number), 'ether')
print("RBTC Balance of (MOC Contract): {0} balance: {1} blockNumber: {2}".format(
    moc_address,
    balance,
    block_number))

# SC BPRO CONTRACT
balance = bpro_token.total_supply(block_identifier=block_number)
print("BPRO Balance of (BPRO Contract): {0} balance: {1} blockNumber: {2}".format(
    bpro_token.address(),
    balance,
    block_number))


# Block Number
block_number = 2609808
print("")
print("BLOCK NUMBER: {0}".format(block_number))
print("--------------------")

balance = Web3.fromWei(network_manager.balance_block_number(user_address, block_number=block_number), 'ether')
print("RBTC Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

# BPRO user address
balance = bpro_token.balance_of(user_address, block_identifier=block_number)
print("BPRO Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

balance = Web3.fromWei(network_manager.balance_block_number(moc_address, block_number=block_number), 'ether')
print("RBTC Balance of (MOC Contract): {0} balance: {1} blockNumber: {2}".format(
    moc_address,
    balance,
    block_number))

# SC BPRO CONTRACT
balance = bpro_token.total_supply(block_identifier=block_number)
print("BPRO Balance of (BPRO Contract): {0} balance: {1} blockNumber: {2}".format(
    bpro_token.address(),
    balance,
    block_number))


# Block Number
block_number = 2614027
print("")
print("BLOCK NUMBER: {0}".format(block_number))
print("--------------------")

balance = Web3.fromWei(network_manager.balance_block_number(user_address, block_number=block_number), 'ether')
print("RBTC Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

# BPRO user address
balance = bpro_token.balance_of(user_address, block_identifier=block_number)
print("BPRO Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

balance = Web3.fromWei(network_manager.balance_block_number(moc_address, block_number=block_number), 'ether')
print("RBTC Balance of (MOC Contract): {0} balance: {1} blockNumber: {2}".format(
    moc_address,
    balance,
    block_number))

# SC BPRO CONTRACT
balance = bpro_token.total_supply(block_identifier=block_number)
print("BPRO Balance of (BPRO Contract): {0} balance: {1} blockNumber: {2}".format(
    bpro_token.address(),
    balance,
    block_number))



# Block Number
block_number = 2614028
print("")
print("BLOCK NUMBER: {0}".format(block_number))
print("--------------------")

balance = Web3.fromWei(network_manager.balance_block_number(user_address, block_number=block_number), 'ether')
print("RBTC Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

# BPRO user address
balance = bpro_token.balance_of(user_address, block_identifier=block_number)
print("BPRO Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

balance = Web3.fromWei(network_manager.balance_block_number(moc_address, block_number=block_number), 'ether')
print("RBTC Balance of (MOC Contract): {0} balance: {1} blockNumber: {2}".format(
    moc_address,
    balance,
    block_number))

# SC BPRO CONTRACT
balance = bpro_token.total_supply(block_identifier=block_number)
print("BPRO Balance of (BPRO Contract): {0} balance: {1} blockNumber: {2}".format(
    bpro_token.address(),
    balance,
    block_number))


# Block Number
block_number = 2621250
print("")
print("BLOCK NUMBER: {0}".format(block_number))
print("--------------------")

balance = Web3.fromWei(network_manager.balance_block_number(user_address, block_number=block_number), 'ether')
print("RBTC Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

# BPRO user address
balance = bpro_token.balance_of(user_address, block_identifier=block_number)
print("BPRO Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

balance = Web3.fromWei(network_manager.balance_block_number(moc_address, block_number=block_number), 'ether')
print("RBTC Balance of (MOC Contract): {0} balance: {1} blockNumber: {2}".format(
    moc_address,
    balance,
    block_number))

# SC BPRO CONTRACT
balance = bpro_token.total_supply(block_identifier=block_number)
print("BPRO Balance of (BPRO Contract): {0} balance: {1} blockNumber: {2}".format(
    bpro_token.address(),
    balance,
    block_number))


# Block Number
block_number = 2621251
print("")
print("BLOCK NUMBER: {0}".format(block_number))
print("--------------------")

balance = Web3.fromWei(network_manager.balance_block_number(user_address, block_number=block_number), 'ether')
print("RBTC Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

# BPRO user address
balance = bpro_token.balance_of(user_address, block_identifier=block_number)
print("BPRO Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

balance = Web3.fromWei(network_manager.balance_block_number(moc_address, block_number=block_number), 'ether')
print("RBTC Balance of (MOC Contract): {0} balance: {1} blockNumber: {2}".format(
    moc_address,
    balance,
    block_number))

# SC BPRO CONTRACT
balance = bpro_token.total_supply(block_identifier=block_number)
print("BPRO Balance of (BPRO Contract): {0} balance: {1} blockNumber: {2}".format(
    bpro_token.address(),
    balance,
    block_number))


# Block Number
block_number = 2621252
print("")
print("BLOCK NUMBER: {0}".format(block_number))
print("--------------------")

balance = Web3.fromWei(network_manager.balance_block_number(user_address, block_number=block_number), 'ether')
print("RBTC Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

# BPRO user address
balance = bpro_token.balance_of(user_address, block_identifier=block_number)
print("BPRO Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

balance = Web3.fromWei(network_manager.balance_block_number(moc_address, block_number=block_number), 'ether')
print("RBTC Balance of (MOC Contract): {0} balance: {1} blockNumber: {2}".format(
    moc_address,
    balance,
    block_number))

# SC BPRO CONTRACT
balance = bpro_token.total_supply(block_identifier=block_number)
print("BPRO Balance of (BPRO Contract): {0} balance: {1} blockNumber: {2}".format(
    bpro_token.address(),
    balance,
    block_number))



# Block Number
block_number = 2621257
print("")
print("BLOCK NUMBER: {0}".format(block_number))
print("--------------------")

balance = Web3.fromWei(network_manager.balance_block_number(user_address, block_number=block_number), 'ether')
print("RBTC Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

# BPRO user address
balance = bpro_token.balance_of(user_address, block_identifier=block_number)
print("BPRO Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

balance = Web3.fromWei(network_manager.balance_block_number(moc_address, block_number=block_number), 'ether')
print("RBTC Balance of (MOC Contract): {0} balance: {1} blockNumber: {2}".format(
    moc_address,
    balance,
    block_number))

# SC BPRO CONTRACT
balance = bpro_token.total_supply(block_identifier=block_number)
print("BPRO Balance of (BPRO Contract): {0} balance: {1} blockNumber: {2}".format(
    bpro_token.address(),
    balance,
    block_number))


# Block Number
block_number = 2621258
print("")
print("BLOCK NUMBER: {0}".format(block_number))
print("--------------------")

balance = Web3.fromWei(network_manager.balance_block_number(user_address, block_number=block_number), 'ether')
print("RBTC Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

# BPRO user address
balance = bpro_token.balance_of(user_address, block_identifier=block_number)
print("BPRO Balance of: {0} balance: {1} blockNumber: {2}".format(
    user_address,
    balance,
    block_number))

balance = Web3.fromWei(network_manager.balance_block_number(moc_address, block_number=block_number), 'ether')
print("RBTC Balance of (MOC Contract): {0} balance: {1} blockNumber: {2}".format(
    moc_address,
    balance,
    block_number))

# SC BPRO CONTRACT
balance = bpro_token.total_supply(block_identifier=block_number)
print("BPRO Balance of (BPRO Contract): {0} balance: {1} blockNumber: {2}".format(
    bpro_token.address(),
    balance,
    block_number))


# finally disconnect from network
network_manager.disconnect()
