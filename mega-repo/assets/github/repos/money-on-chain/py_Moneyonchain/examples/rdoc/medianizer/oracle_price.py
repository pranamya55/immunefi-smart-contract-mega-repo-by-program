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
config_network = 'rdocTestnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


print("Connecting to RDOC Main Contract")
moc_contract = RDOCMoC(network_manager).from_abi()

#oracle_provider = moc_contract.sc_moc_state.price_provider()
#print("Oracle address: {0}".format(oracle_provider))

#oracle_provider = '0x987ccC60c378a61d167B6DD1EEF7613c6f63938f'
#oracle_provider = '0xDC3551f16FfDeBAa3Cb8D3b6C16d2A5bB9646dA4'

#oracle = RDOCMoCMedianizer(connection_manager, contract_address=oracle_provider)
oracle = RDOCMoCMedianizer(network_manager).from_abi()
print("RIF Price in USD: {0}".format(oracle.price()))

# finally disconnect from network
network_manager.disconnect()
