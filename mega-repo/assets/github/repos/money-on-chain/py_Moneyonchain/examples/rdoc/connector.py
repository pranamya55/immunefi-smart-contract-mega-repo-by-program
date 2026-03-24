from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoC


connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnetAlpha'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_moc = RDOCMoC(network_manager).from_abi()
print("Connector: {0}".format(moc_moc.connector()))

print("Addresses: {0}".format(moc_moc.connector_addresses()))

# finally disconnect from network
network_manager.disconnect()
