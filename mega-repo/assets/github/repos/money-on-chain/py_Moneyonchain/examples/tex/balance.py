
from web3 import Web3
from moneyonchain.networks import NetworkManager


connection_network='rskTestnetPublic'
config_network = 'dexTestnet'

# init network manager
# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager = NetworkManager(
    connection_network=connection_network,
    config_network=config_network)

# run install() if is the first time and you want to install
# networks connection from brownie
# network_manager.install()

# Connect to network
network_manager.connect()


print(Web3.fromWei(network_manager.network_balance("0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3"), 'ether'))

# finally disconnect from network
network_manager.disconnect()