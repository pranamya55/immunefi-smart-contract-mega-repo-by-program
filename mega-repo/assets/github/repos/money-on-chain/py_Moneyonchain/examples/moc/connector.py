from moneyonchain.networks import network_manager
from moneyonchain.moc import MoC


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_moc = MoC(network_manager, load_sub_contract=False).from_abi().contracts_discovery()

print("Connector: {0}".format(moc_moc.connector()))

print("Addresses: {0}".format(moc_moc.connector_addresses()))

# finally disconnect from network
network_manager.disconnect()
