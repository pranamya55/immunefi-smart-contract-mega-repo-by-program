"""
Oracle price get current oracle from MOC
"""

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoC
from moneyonchain.medianizer import MoCMedianizer

# Network types
#
# mocTestnet: Testnet
# mocMainnet2: Production Mainnet


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

print("Connecting to MoC Main Contract")
moc_contract = MoC(network_manager).from_abi()

oracle_provider = moc_contract.sc_moc_state.price_provider()
print("Oracle address: {0}".format(oracle_provider))

oracle = MoCMedianizer(network_manager, contract_address=oracle_provider).from_abi()

print("Bitcoin Price in USD: {0}".format(oracle.price()))

# finally disconnect from network
network_manager.disconnect()
