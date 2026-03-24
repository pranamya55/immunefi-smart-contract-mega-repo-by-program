from moneyonchain.networks import network_manager
from moneyonchain.tex import MoCDecentralizedExchange

connection_network = 'rskTestnetPublic'
config_network = 'dexTestnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


print("Connecting to MoCDecentralizedExchange")
dex = MoCDecentralizedExchange(network_manager).from_abi()
print(dex.token_pairs())

pair = ['0xCB46c0ddc60D18eFEB0E586C17Af6ea36452Dae0', '0x4dA7997A819bb46B6758B9102234c289dD2Ad3bf']
tx_receipt = dex.run_tick_for_pair(pair)

print("Done!")

# finally disconnect from network
network_manager.disconnect()
