from moneyonchain.networks import NetworkManager
from moneyonchain.tex import MoCDecentralizedExchange


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

print("Connecting to MoCDecentralizedExchange")
dex = MoCDecentralizedExchange(network_manager).from_abi()

print(dex.min_order_amount())

# finally disconnect from network
network_manager.disconnect()
