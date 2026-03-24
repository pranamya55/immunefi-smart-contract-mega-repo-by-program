"""
Proxy implementation
"""

from web3 import Web3
from moneyonchain.networks import network_manager
from moneyonchain.governance import ProxyAdmin


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


contract_admin = ProxyAdmin(network_manager)
contract_address = Web3.toChecksumAddress(network_manager.options['networks'][config_network]['addresses']['MoC'])
print(contract_admin.implementation(contract_address))

# finally disconnect from network
network_manager.disconnect()
