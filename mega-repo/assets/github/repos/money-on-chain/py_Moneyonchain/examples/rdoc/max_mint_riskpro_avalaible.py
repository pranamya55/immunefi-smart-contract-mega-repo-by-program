from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoCState


connection_network = 'rskMainnetPublic'
config_network = 'rdocMainnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


moc_state = RDOCMoCState(network_manager).from_abi()

print("Max Mint RiskPro setted: {0}".format(moc_state.max_mint_bpro()))
print("Max mint RiskPro available: {0}".format(moc_state.max_mint_bpro_available()))

# finally disconnect from network
network_manager.disconnect()
