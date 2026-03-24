import json
import os
from moneyonchain.networks import NetworkManager
from moneyonchain.tokens import DoCToken, WRBTCToken, BProToken, RIFDoC, RIF, RIFPro

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/allowance_info.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


def options_from_settings(filename='settings.json'):
    """ Options from file settings.json """

    with open(filename) as f:
        config_options = json.load(f)

    return config_options


connection_network = 'rskTestnetPublic'
config_network = 'dexTestnet'

# init network manager
# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager = NetworkManager(
    connection_network=connection_network,
    config_network=config_network)

# run install() if is the first time and you want to install
# networks connection from brownie
# network_manager.install()

# Connect to network
network_manager.connect()


# load settings from file
settings = options_from_settings(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json'))

#account = '0xB5E2Bed9235b6366Fa0254c2e6754E167e0a2383'
account = '0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3'
dex_address = network_manager.options['networks'][config_network]['addresses']['dex']


def print_info(contract_token):
    print("TOKEN INFO")
    print("==========")
    print("Token Name: {0}".format(contract_token.name()))
    print("Token Symbol: {0}".format(contract_token.symbol()))
    print("Total Supply: {0}".format(contract_token.total_supply()))
    print("")
    print("BALANCES")
    print("==========")
    print("Balance: {0} {1}".format(contract_token.balance_of(account), contract_token.symbol()))
    print("Allowance: {0} {1}".format(contract_token.allowance(account, dex_address), contract_token.symbol()))
    print()
    print()


# DOC
token_sc = DoCToken(network_manager, contract_address=settings[config_network]['DOC']).from_abi()
print_info(token_sc)

# BPRO
token_sc = BProToken(network_manager, contract_address=settings[config_network]['BPRO']).from_abi()
print_info(token_sc)

# WRBTC
token_sc = WRBTCToken(network_manager, contract_address=settings[config_network]['WRBTC']).from_abi()
print_info(token_sc)

# RDOC
token_sc = RIFDoC(network_manager, contract_address=settings[config_network]['RDOC']).from_abi()
print_info(token_sc)

# RIF
token_sc = RIF(network_manager, contract_address=settings[config_network]['RIF']).from_abi()
print_info(token_sc)

# RIFP
token_sc = RIFPro(network_manager, contract_address=settings[config_network]['RIFP']).from_abi()
print_info(token_sc)
