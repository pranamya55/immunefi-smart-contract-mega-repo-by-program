"""
 brownie networks add BSCNetwork bscTestnet host=https://data-seed-prebsc-1-s1.binance.org:8545/ chainid=97 explorer=https://blockscout.com/rsk/mainnet/api
 brownie networks add BSCNetwork bscTestnetPrivate host=http://localhost:8575/ chainid=97 explorer=https://blockscout.com/rsk/mainnet/api
"""

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoC

connection_network = 'bscTestnetPrivate'
config_network = 'bscMoCAlphaTestnet'

# Connect to network
network_manager.connect(
    connection_network=connection_network,
    config_network=config_network)

print(network_manager.is_connected())

moc_main = MoC(network_manager, contract_address='0xC0321b74Ce197FFCBA1c88bdFA36B046De6F7ADF', load_sub_contract=False).from_abi()

print(moc_main.connector())

# finally disconnect from network
network_manager.disconnect()
