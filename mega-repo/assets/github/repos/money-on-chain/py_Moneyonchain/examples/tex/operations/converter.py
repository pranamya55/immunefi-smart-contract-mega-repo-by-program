"""

"""

import json
import os
from moneyonchain.manager import ConnectionManager
from moneyonchain.dex import MoCDecentralizedExchange


def options_from_settings(filename='settings.json'):
    """ Options from file settings.json """

    with open(filename) as f:
        config_options = json.load(f)

    return config_options


network = 'dexTestnet'
connection_manager = ConnectionManager(network=network)
print("Connecting to %s..." % network)
print("Connected: {conectado}".format(conectado=connection_manager.is_connected))

# load settings from file
settings = options_from_settings(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'))

print("Connecting to MoCDecentralizedExchange")
dex = MoCDecentralizedExchange(connection_manager)

base_token = settings[network]['WRBTC']
secondary_token = settings[network]['DOC']

amount = int(1 * 10 ** 18)

#print(dex.convert_token_to_common_base(secondary_token, amount, base_token))
print(dex.convert_token_to_common_base(base_token, amount, secondary_token))

#print(dex.token_pairs_status(base_token, secondary_token))
