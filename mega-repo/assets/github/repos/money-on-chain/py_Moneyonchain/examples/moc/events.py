from moneyonchain.networks import NetworkManager
from moneyonchain.moc import MoC, MoCExchange, MoCExchangeRiskProMint

connection_network = 'rskTesnetLocal'
config_network = 'mocTestnetAlpha'

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

print(network_manager.is_connected())

moc_contract = MoC(network_manager).from_abi()


moc_exchange = MoCExchange(network_manager).from_abi()

events = moc_exchange.filter_events(from_block=1435736, to_block=1445760)
for event in events:
    eve = MoCExchangeRiskProMint(event)
    eve.print_table()

# finally disconnect from network
network_manager.disconnect()
