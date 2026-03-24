"""
Prices in enviroments from RDOC
"""

from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoC

# Network types
#
# rdocTestnet: Testnet
# rdocMainnet: Production Mainnet


connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnetAlpha'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


print("Connecting to RDOC Main Contract")
moc_contract = RDOCMoC(network_manager).from_abi()

print("RIF Price in USD: {0}".format(moc_contract.sc_moc_state.bitcoin_price()))
print("RIF Moving Average in USD: {0}".format(moc_contract.sc_moc_state.bitcoin_moving_average()))

# finally disconnect from network
network_manager.disconnect()
