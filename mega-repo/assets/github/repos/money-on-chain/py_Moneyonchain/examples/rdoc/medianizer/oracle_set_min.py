"""
Oracle price get current oracle from MOC
"""

from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoC
from moneyonchain.medianizer import RDOCMoCMedianizer

# Network types
#
# rdocTestnet: Testnet
# rdocMainnet: Production Mainnet


connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnetAlpha'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


oracle_provider = '0xDC3551f16FfDeBAa3Cb8D3b6C16d2A5bB9646dA4'
oracle = RDOCMoCMedianizer(network_manager, contract_address=oracle_provider).from_abi()

print("RIF Price in USD: {0}".format(oracle.price()))
print("Min: {0}".format(oracle.min()))

# finally disconnect from network
network_manager.disconnect()
