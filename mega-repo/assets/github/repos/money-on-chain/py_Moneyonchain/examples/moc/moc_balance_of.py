from moneyonchain.networks import NetworkManager
from moneyonchain.moc import MoC

connection_network='rskTestnetPublic'
config_network = 'mocTestnet'

# init network manager
# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager = NetworkManager(
    connection_network=connection_network,
    config_network=config_network)

# Connect to network
network_manager.connect()
moc_main = MoC(network_manager).from_abi()

res = moc_main.moc_balance_of("0xcd8a1c9acc980ae031456573e34dc05cd7dae6e3")
print(res)

# finally disconnect from network
network_manager.disconnect()
