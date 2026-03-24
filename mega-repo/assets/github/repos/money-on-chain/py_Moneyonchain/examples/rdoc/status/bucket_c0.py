from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoCState

connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnetAlpha'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


moc_state = RDOCMoCState(network_manager).from_abi()

print("Bucket NBTC: {0}".format(moc_state.bucket_nbtc(str.encode('C0'), formatted=False)))
print("Bucket NDOC: {0}".format(moc_state.bucket_ndoc(str.encode('C0'), formatted=False)))

# finally disconnect from network
network_manager.disconnect()