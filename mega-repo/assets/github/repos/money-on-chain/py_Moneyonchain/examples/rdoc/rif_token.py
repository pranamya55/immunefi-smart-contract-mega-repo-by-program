from moneyonchain.networks import network_manager
from moneyonchain.tokens import RIF, RIFPro, RIFDoC

connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


account = '0xCD8a1C9aCC980Ae031456573e34Dc05CD7dAE6e3'

print("Connecting to RIF TOKEN")
rif_token = RIF(network_manager)
print("Token Name: {0}".format(rif_token.name()))
print("Token Symbol: {0}".format(rif_token.symbol()))
print("Total Supply: {0}".format(rif_token.total_supply()))
print("Account: {0} Balance RIF: {1}".format(account, rif_token.balance_of(account, block_identifier=1442600)))
print(rif_token.address())


doc_token = RIFDoC(network_manager)
print("Token Name: {0}".format(doc_token.name()))
print("Token Symbol: {0}".format(doc_token.symbol()))
print("Total Supply: {0}".format(doc_token.total_supply()))
print("Account: {0} Balance DOC: {1}".format(account, doc_token.balance_of(account, block_identifier=1442000)))
print(doc_token.address())


rifp_token = RIFPro(network_manager)
print("Token Name: {0}".format(rifp_token.name()))
print("Token Symbol: {0}".format(rifp_token.symbol()))
print("Total Supply: {0}".format(rifp_token.total_supply()))
print("Account: {0} Balance DOC: {1}".format(account, rifp_token.balance_of(account)))
print(rifp_token.address())

# finally disconnect from network
network_manager.disconnect()
