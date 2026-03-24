"""
Proxy implementation
"""

from web3 import Web3
from moneyonchain.networks import network_manager
from moneyonchain.governance import ProxyAdmin


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

#proxy_address = '0x01AD6f8E884ed4DDC089fA3efC075E9ba45C9039'
#block_identifier = 1743680

#proxy_address = '0x9c1e20A0Ea6c71B0AEA47fd8B1E29de208ab7A82'
proxy_address = '0xC003A2e210FA3E2fBdDcf564Fe0E1bbCd93E3B40'
block_identifier = 2326844 #70

contract_admin = ProxyAdmin(network_manager).from_abi()
print("Proxy: {0} Implementation:{1} Block: {2} ".format(
    proxy_address,
    contract_admin.implementation(Web3.toChecksumAddress(proxy_address), block_identifier=block_identifier),
    block_identifier))

# finally disconnect from network
network_manager.disconnect()
