
import json
from moneyonchain.networks import network_manager
from moneyonchain.tex import MoCDecentralizedExchange


def options_from_settings(filename='settings.json'):
    """ Options from file settings.json """

    with open(filename) as f:
        config_options = json.load(f)

    return config_options


connection_network = 'rskTestnetPublic'
config_network = 'dexTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

# load settings from file
settings = options_from_settings()

settings_pair = settings[config_network]['BPRO/FLIP']

base_token = settings_pair['baseToken']
secondary_token = settings_pair['secondaryToken']

dex = MoCDecentralizedExchange(network_manager).from_abi()

print("TICK STATUS")
print("==========")
print(dex.token_pairs_status(base_token, secondary_token))
print("TICK STAGE")
print("==========")
print(dex.tick_stage((base_token, secondary_token)))
print("SELL ORDER LENGHT")
print("=================")
print(dex.sell_orders_length((base_token, secondary_token)))
print("BUY ORDER LENGHT")
print("=================")
print(dex.buy_orders_length((base_token, secondary_token)))

print("PENDING SELL ORDER LENGHT")
print("=================")
print(dex.pending_sell_orders_length((base_token, secondary_token)))
print("PENDING  BUY ORDER LENGHT")
print("=================")
print(dex.pending_buy_orders_length((base_token, secondary_token)))



# finally disconnect from network
network_manager.disconnect()
