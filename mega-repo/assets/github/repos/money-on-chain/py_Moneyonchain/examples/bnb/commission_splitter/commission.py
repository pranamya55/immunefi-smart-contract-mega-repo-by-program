"""
To run this script need private key, run this scripts with:

user> export ACCOUNT_PK_SECRET=PK
user> python ./mint_bpro.py

Where replace with your PK, and also you need to have funds in this account
"""


from decimal import Decimal
from web3 import Web3

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoCInrate, CommissionSplitter

connection_network = 'bscTestnetPrivate'
config_network = 'bnbTestnet'

# Connect to network
network_manager.connect(
    connection_network=connection_network,
    config_network=config_network)


moc_inrate = MoCInrate(network_manager).from_abi()
splitter = CommissionSplitter(network_manager, contract_address='0x5F1984BdFB81EbA96E95693a08Aec4B5C853Da0C').from_abi()

print("Multisig address: [{0}]".format(splitter.commission_address()))
print("MoC Address: [{0}]".format(splitter.moc_address()))
print("MoCInrate Target commission: [{0}] (have to be the splitter)".format(moc_inrate.commission_address()))
print("Proportion: [{0}]".format(Web3.fromWei(splitter.moc_proportion(), 'ether')))
print("Balance: [{0}]".format(splitter.balance()))
print("MoC Token: [{0}]".format(splitter.moc_token()))
print("MoC Token Address commission: [{0}]".format(splitter.moc_token_commission_address()))



# finally disconnect from network
network_manager.disconnect()
