"""
To run this script need private key, run this scripts with:

user> export ACCOUNT_PK_SECRET=fdas46f4dsafds7f89ds7f8dafd4fdsaf3dsA4ds5a
user> python ./example_moc_mint_bpro.py

Where replace with your PK, and also you need to have funds in this account
"""


from decimal import Decimal
from web3 import Web3
from moneyonchain.networks import network_manager
from moneyonchain.moc import MoC


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_main = MoC(network_manager).from_abi()

# This transaction is not async, you have to wait to the transaction is mined
print("Please wait to the transaction be mined!...")
tx_receipt = moc_main.reedeem_all_doc()

# finally disconnect from network
network_manager.disconnect()
