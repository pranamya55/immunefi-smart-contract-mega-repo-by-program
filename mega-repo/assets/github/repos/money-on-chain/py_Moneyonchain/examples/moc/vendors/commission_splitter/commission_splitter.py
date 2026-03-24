import json
from web3 import Web3

from moneyonchain.networks import network_manager
from moneyonchain.governance import Governed
from moneyonchain.moc_vendors import VENDORSMoCInrate, VENDORSCommissionSplitter
from moneyonchain.tokens import MoCToken


import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/commission_splitter.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


# Connect to network
network_manager.connect(connection_network='rskTestnetPublic', config_network='mocTestnetAlpha')


splitter = VENDORSCommissionSplitter(network_manager).from_abi()
governed = Governed(network_manager, contract_address=splitter.address()).from_abi()

moc_inrate = VENDORSMoCInrate(network_manager).from_abi()
moc_token = MoCToken(network_manager).from_abi()

info_dict = dict()
info_dict['proportion'] = dict()
info_dict['balance'] = dict()
info_dict['balance_moc'] = dict()

splitter_address = splitter.address()

log.info("Splitter Address: [{0}]".format(splitter_address))
log.info("Owner: {}".format(splitter.implementation()))
log.info("Governor: [{0}]".format(governed.governor()))
log.info("FLOW BTC2MOC address: [{0}]".format(splitter.commission_address()))
log.info("FLOW BitproRewardsBuffer address: [{0}]".format(splitter.moc_token_commission_address()))
log.info("MoC OS Address: [{0}]".format(splitter.moc_address()))
log.info("MoCInrate Target commission: [{0}] (have to be the splitter)".format(moc_inrate.commission_address()))

info_dict['proportion']['moc'] = Web3.fromWei(splitter.moc_proportion(), 'ether')
info_dict['proportion']['multisig'] = 1 - info_dict['proportion']['moc']

log.info("Proportion to BITPRO (MOC OS): [{0}]".format(info_dict['proportion']['moc']))
log.info("Proportion FLOW BTC2MOC: [{0}]".format(info_dict['proportion']['multisig']))

info_dict['balance']['splitter'] = splitter.balance()
log.info("Splitter balance RBTC: [{0}]".format(info_dict['balance']['splitter']))

info_dict['balance_moc']['splitter'] = moc_token.balance_of(splitter_address)
log.info("Splitter balance MOC: [{0}]".format(info_dict['balance_moc']['splitter']))

# balances moc
balance = Web3.fromWei(network_manager.network_balance(splitter.moc_address()), 'ether')
info_dict['balance']['moc'] = balance
log.info("MoC OS balance (proportion: {0}): [{1}]".format(info_dict['proportion']['moc'],
                                                    info_dict['balance']['moc']))

# balances flow BTC2MOC
balance = Web3.fromWei(network_manager.network_balance(splitter.commission_address()), 'ether')
info_dict['balance']['commission'] = balance
log.info("FLOW BTC2MOC balance (proportion: {0}): [{1}]".format(info_dict['proportion']['multisig'],
                                                         info_dict['balance']['commission']))

# balances flow BitproRewardsBuffer
balance = moc_token.balance_of(splitter.moc_token_commission_address())
info_dict['balance_moc']['moc'] = balance
log.info("FLOW BitproRewardsBuffer balance MOC (proportion: {0}): [{1}]".format(info_dict['proportion']['moc'],
                                                    info_dict['balance_moc']['moc']))

# finally disconnect from network
network_manager.disconnect()
