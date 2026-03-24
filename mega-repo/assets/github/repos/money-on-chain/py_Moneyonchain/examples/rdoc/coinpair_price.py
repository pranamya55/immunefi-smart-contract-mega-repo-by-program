"""
Coin pair price
"""

from moneyonchain.networks import network_manager
from moneyonchain.oracle import CoinPairPrice


connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnetAlpha'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

contract = CoinPairPrice(network_manager).from_abi()
print(contract.price())

# finally disconnect from network
network_manager.disconnect()