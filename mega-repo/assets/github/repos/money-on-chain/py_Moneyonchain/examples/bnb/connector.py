"""
 brownie networks add BSCNetwork bscTestnet host=https://data-seed-prebsc-1-s1.binance.org:8545/ chainid=97 explorer=https://blockscout.com/rsk/mainnet/api
"""

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoC, MoCConnector


connection_network = 'bscTestnet'
config_network = 'bnbAlphaTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_moc = MoC(network_manager, contract_address='0xC0321b74Ce197FFCBA1c88bdFA36B046De6F7ADF', load_sub_contract=False).from_abi()

print("Connector: {0}".format(moc_moc.connector()))

moc_connector = MoCConnector(network_manager, contract_address='0x17b5772510B4dE74380D0df8FbdC36C05fe29A6A').from_abi()

print("Addresses: {0}".format(moc_connector.contracts_addresses()))

# finally disconnect from network
network_manager.disconnect()
