import json
import os
from moneyonchain.networks import network_manager
from moneyonchain.tex import MoCDecentralizedExchange


def options_from_settings(filename='settings.json'):
    """ Options from file settings.json """

    with open(filename) as f:
        config_options = json.load(f)

    return config_options


connection_network='rskMainnetPublic'
config_network = 'dexMainnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

# load settings from file
settings = options_from_settings(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'))

print("Connecting to MoCDecentralizedExchange")
dex = MoCDecentralizedExchange(network_manager).from_abi()

base_token = settings[config_network]['DOC']
secondary_token = settings[config_network]['WRBTC']

print(dex.token_pairs_status(base_token, secondary_token))

# finally disconnect from network
network_manager.disconnect()