"""
Deploy Price Provider WRBTC/MoC
"""

from moneyonchain.networks import network_manager
from moneyonchain.tex import TexMocBtcPriceProviderFallback

connection_network = 'rskTestnetPublic'
config_network = 'dexTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

# Price provider address
contract_address = '0x7aBF17256c7A03E20E774673a9eCCe10919fd36F'

price_provider = TexMocBtcPriceProviderFallback(network_manager, contract_address=contract_address).from_abi()
print(price_provider.peek())

# finally disconnect from network
network_manager.disconnect()
