"""
 brownie networks add BSCNetwork bscTestnet host=https://data-seed-prebsc-1-s1.binance.org:8545/ chainid=97 explorer=https://blockscout.com/rsk/mainnet/api
"""

from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoC, RDOCMoCConnector


connection_network = 'bscTestnet'
config_network = 'btcbAlphaTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_moc = RDOCMoC(network_manager, contract_address='0x88DF76BEe402a1Bc152d5C53f04E631ac50242a8', load_sub_contract=False).from_abi()

print("Connector: {0}".format(moc_moc.connector()))

moc_connector = RDOCMoCConnector(network_manager, contract_address='0x1d8f5769F6b53F60B2d304167C43C6C481ae1528').from_abi()

print("Addresses: {0}".format(moc_connector.contracts_addresses()))

# finally disconnect from network
network_manager.disconnect()
