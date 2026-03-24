"""
Deploy Price Provider DOC/MoC

Alpha-testnet: 0x50E837429561884E94134715D2a93827f0861630
Testnet: 0x8DCE78BbD4D757EF7777Be113277cf5A35283b1E
Mainnet: 0x72835fDc4F73cb33b1E7e03bFe067AAfED2BDB9C

"""

from moneyonchain.networks import network_manager
from moneyonchain.tex import TokenPriceProviderLastClosingPrice

connection_network = 'rskTestnetPublic'
config_network = 'dexTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

# Price provider address
contract_address = '0x50E837429561884E94134715D2a93827f0861630'

price_provider = TokenPriceProviderLastClosingPrice(network_manager, contract_address=contract_address).from_abi()
print(price_provider.peek())

# finally disconnect from network
network_manager.disconnect()
