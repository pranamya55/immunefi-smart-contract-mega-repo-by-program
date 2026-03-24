from moneyonchain.networks import network_manager
from moneyonchain.moc import MoCState

connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


print("Connecting to MoCState...")
moc_state = MoCState(network_manager).from_abi()

print("Max Mint BPRO setted: {0}".format(moc_state.max_mint_bpro()))
print("Max mint BPRO avalaible: {0}".format(moc_state.max_mint_bpro_available()))

# finally disconnect from network
network_manager.disconnect()
