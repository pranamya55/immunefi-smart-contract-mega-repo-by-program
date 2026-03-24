from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoCState, RDOCMoC

connection_network = 'rskMainnetPublic'
config_network = 'rdocMainnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


moc_state = RDOCMoCState(network_manager).from_abi()
print(moc_state.collateral_reserves())

# finally disconnect from network
network_manager.disconnect()
