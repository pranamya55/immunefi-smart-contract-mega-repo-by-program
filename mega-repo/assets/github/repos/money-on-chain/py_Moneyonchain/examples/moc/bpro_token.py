from moneyonchain.networks import network_manager
from moneyonchain.tokens import BProToken


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

account = '0xCD8a1C9aCC980Ae031456573e34Dc05CD7dAE6e3'

print("Connecting to BProToken")
bpro_token = BProToken(network_manager).from_abi()
print("Token Name: {0}".format(bpro_token.name()))
print("Token Symbol: {0}".format(bpro_token.symbol()))
print("Total Supply: {0}".format(bpro_token.total_supply()))
print("Account: {0} Balance BPro: {1}".format(account, bpro_token.balance_of(account)))
print(bpro_token.address())

# finally disconnect from network
network_manager.disconnect()
