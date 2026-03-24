from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoCState

connection_network = 'rskMainnetPublic'
config_network = 'rdocMainnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


print("Connecting to MoCState")
moc_state = RDOCMoCState(network_manager).from_abi()

print("Bitcoin Price in USD: {0}".format(moc_state.bitcoin_price()))
print("Bitcoin Moving Average in USD: {0}".format(moc_state.bitcoin_moving_average()))
print("Smoothing Factor: {0}".format(moc_state.smoothing_factor()))

# finally disconnect from network
network_manager.disconnect()

