"""
Commission Manager
"""

import json
import os
from tabulate import tabulate

from moneyonchain.networks import network_manager
from moneyonchain.tex import CommissionManager


def options_from_settings(filename='settings.json'):
    """ Options from file settings.json """

    with open(filename) as f:
        config_options = json.load(f)

    return config_options


# load settings from file
settings = options_from_settings(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'))


connection_network = 'rskMainnetPublic'
config_network = 'dexMainnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


dex_commission = CommissionManager(network_manager).from_abi()

titles = ['Storage', 'Value']
display_table = list()
display_table.append(["Beneficiary", dex_commission.beneficiary_address()])
display_table.append(["Commission Rate", str(dex_commission.commision_rate())])
display_table.append(["Cancelation Rate", str(dex_commission.cancelation_penalty_rate())])
display_table.append(["Expiration Rate", str(dex_commission.expiration_penalty_rate())])
display_table.append(["Minimum Fix Commision", str(dex_commission.minimum_commission())])
display_table.append(["Fee 0.001 WRBTC", str(dex_commission.calculate_initial_fee(0.001, 10000))])
display_table.append(["Fee 10 DOC", str(dex_commission.calculate_initial_fee(10, 1))])

print(tabulate(display_table, headers=titles, tablefmt="pipe"))
print()

block_identifier = network_manager.block_number

titles = ['Token', 'Balance', 'Address', 'Block N']
display_table = list()

token_name = 'WRBTC'
token = settings[config_network][token_name]
display_table.append([token_name, str(dex_commission.exchange_commissions(token, block_identifier=block_identifier)), token, str(block_identifier)])

token_name = 'DOC'
token = settings[config_network][token_name]
display_table.append([token_name, str(dex_commission.exchange_commissions(token, block_identifier=block_identifier)), token, str(block_identifier)])

token_name = 'BPRO'
token = settings[config_network][token_name]
display_table.append([token_name, str(dex_commission.exchange_commissions(token, block_identifier=block_identifier)), token, str(block_identifier)])

token_name = 'RDOC'
token = settings[config_network][token_name]
display_table.append([token_name, str(dex_commission.exchange_commissions(token, block_identifier=block_identifier)), token, str(block_identifier)])

token_name = 'RIF'
token = settings[config_network][token_name]
display_table.append([token_name, str(dex_commission.exchange_commissions(token, block_identifier=block_identifier)), token, str(block_identifier)])

token_name = 'RIFP'
token = settings[config_network][token_name]
display_table.append([token_name, str(dex_commission.exchange_commissions(token, block_identifier=block_identifier)), token, str(block_identifier)])

token_name = 'MOC'
token = settings[config_network][token_name]
display_table.append([token_name, str(dex_commission.exchange_commissions(token, block_identifier=block_identifier)), token, str(block_identifier)])


print(tabulate(display_table, headers=titles, tablefmt="pipe"))
