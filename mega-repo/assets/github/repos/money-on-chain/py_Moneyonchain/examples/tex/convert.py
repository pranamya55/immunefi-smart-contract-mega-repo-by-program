from moneyonchain.networks import network_manager
from moneyonchain.tex import MoCDecentralizedExchange


connection_network = 'rskTestnetPublic'
config_network = 'dexTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

print("Connecting to MoCDecentralizedExchange")
dex = MoCDecentralizedExchange(network_manager).from_abi()

token_address = '0x0399c7F7B37E21cB9dAE04Fb57E24c68ed0B4635'
amount = int(100 * 10 ** 18)
base_address = '0x09b6ca5E4496238A1F176aEa6Bb607DB96c2286E'

print(dex.convert_token_to_common_base(token_address, amount, base_address))

print(dex.token_pairs_status(base_address, token_address))

# finally disconnect from network
network_manager.disconnect()
