from decimal import Decimal
from web3 import Web3
from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoC


connection_network = 'rskMainnetPublic'
config_network = 'rdocMainnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


print("Connecting to MoC Main Contract")
moc_main = RDOCMoC(network_manager).from_abi()

addresses = moc_main.connector_addresses()
#addresses = moc_main.connector()
print(addresses)

# finally disconnect from network
network_manager.disconnect()
