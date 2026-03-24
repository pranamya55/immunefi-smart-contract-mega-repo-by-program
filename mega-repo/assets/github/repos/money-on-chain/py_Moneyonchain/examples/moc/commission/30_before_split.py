import json
from web3 import Web3

from moneyonchain.networks import NetworkManager
from moneyonchain.governance import Governed
from moneyonchain.moc import MoCInrate, CommissionSplitter


import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/30_before_split.log',
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


connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'

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
settings = options_from_settings()

contact_address = settings[config_network]['CommissionSplitter']

governed = Governed(network_manager, contract_address=contact_address).from_abi()
splitter = CommissionSplitter(network_manager, contract_address=contact_address).from_abi()
moc_inrate = MoCInrate(network_manager).from_abi()

info_dict = dict()
info_dict['proportion'] = dict()
info_dict['balance'] = dict()

log.info("Splitter Address: [{0}]".format(contact_address))
log.info("Governor: [{0}]".format(governed.governor()))
log.info("Multisig address: [{0}]".format(splitter.commission_address()))
log.info("MoC Address: [{0}]".format(splitter.moc_address()))
log.info("MoCInrate Target commission: [{0}] (have to be the splitter)".format(moc_inrate.commission_address()))

info_dict['proportion']['moc'] = Web3.fromWei(splitter.moc_proportion(), 'ether')
info_dict['proportion']['multisig'] = 1 - info_dict['proportion']['moc']

log.info("Proportion MOC: [{0}]".format(info_dict['proportion']['moc']))
log.info("Proportion Multisig: [{0}]".format(info_dict['proportion']['multisig']))

info_dict['balance']['splitter'] = splitter.balance()
log.info("Splitter balance: [{0}]".format(info_dict['balance']['splitter']))

# balances commision
balance = Web3.fromWei(network_manager.network_balance(splitter.commission_address()), 'ether')
info_dict['balance']['commission'] = balance
log.info("Multisig balance (proportion: {0}): [{1}]".format(info_dict['proportion']['multisig'],
                                                         info_dict['balance']['commission']))

# balances moc
balance = Web3.fromWei(network_manager.network_balance(splitter.moc_address()), 'ether')
info_dict['balance']['moc'] = balance
log.info("MoC balance (proportion: {0}): [{1}]".format(info_dict['proportion']['moc'],
                                                    info_dict['balance']['moc']))

# finally disconnect from network
network_manager.disconnect()
