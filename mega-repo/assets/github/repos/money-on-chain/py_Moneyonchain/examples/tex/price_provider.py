from moneyonchain.networks import network_manager
from moneyonchain.tex import MoCDecentralizedExchange


connection_network='rskMainnetPublic'
config_network = 'dexMainnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

print("Connecting to MoCDecentralizedExchange")
dex = MoCDecentralizedExchange(network_manager).from_abi()

base_address = '0xe700691dA7b9851F2F35f8b8182c69c53CcaD9Db'
secondary_address = '0x967f8799aF07DF1534d48A95a5C9FEBE92c53ae0'
print(dex.get_price_provider(base_address, secondary_address))

# finally disconnect from network
network_manager.disconnect()
