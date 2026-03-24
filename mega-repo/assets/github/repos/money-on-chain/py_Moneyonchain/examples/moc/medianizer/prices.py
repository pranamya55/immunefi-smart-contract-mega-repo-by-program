"""
Prices in enviroments from MOC
"""

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoC

# Network types
#
# mocTestnet: Testnet
# mocMainnet2: Production Mainnet


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


print("Connecting to MoC Main Contract")
moc_contract = MoC(network_manager).from_abi()

print("Bitcoin Price in USD: {0}".format(moc_contract.sc_moc_state.bitcoin_price()))
print("Bitcoin Moving Average in USD: {0}".format(moc_contract.sc_moc_state.bitcoin_moving_average()))

# finally disconnect from network
network_manager.disconnect()
