from moneyonchain.networks import network_manager
from moneyonchain.tokens import DoCToken


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

account = '0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3'

print("Connecting to DoCToken")
doc_token = DoCToken(network_manager).from_abi()
print("Token Name: {0}".format(doc_token.name()))
print("Token Symbol: {0}".format(doc_token.symbol()))
print("Total Supply: {0}".format(doc_token.total_supply()))
print("Account: {0} Balance DOC: {1}".format(account, doc_token.balance_of(account)))
print(doc_token.address())

# finally disconnect from network
network_manager.disconnect()
