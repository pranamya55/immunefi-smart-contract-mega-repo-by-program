from moneyonchain.networks import network_manager

connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'

network_manager.add_network(network_host='https://public-node2.testnet.rsk.co')

# # Connect to network
# network_manager.connect(connection_network=connection_network, config_network=config_network)
#
# print(network_manager.is_connected())
#
# # finally disconnect from network
# network_manager.disconnect()
