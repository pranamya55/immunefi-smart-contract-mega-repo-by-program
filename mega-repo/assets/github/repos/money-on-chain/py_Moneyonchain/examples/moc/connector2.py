from moneyonchain.networks import network_manager
from moneyonchain.moc import MoC, MoCConnector


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_moc = MoC(network_manager, load_sub_contract=False).from_abi()
print("Connector address: {0}".format(moc_moc.connector()))

moc_connector = MoCConnector(network_manager, contract_address=moc_moc.connector()).from_abi()
print(moc_connector.sc.whitelist())


# finally disconnect from network
network_manager.disconnect()
