"""
To run this script need private key, run this scripts with:

user> export ACCOUNT_PK_SECRET=PK
user> python ./reedeem_free_doc.py

Where replace with your PK, and also you need to have funds in this account
"""


from decimal import Decimal
from moneyonchain.networks import NetworkManager
from moneyonchain.moc import MoC

connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha3'

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

moc_main = MoC(network_manager).from_abi()

amount = Decimal(1.0)
print("Reedem Free Doc: {0}".format(amount))

# This transaction is not async, you have to wait to the transaction is mined
print("Please wait to the transaction be mined!...")
tx_receipt = moc_main.reedeem_free_doc(amount)

# finally disconnect from network
network_manager.disconnect()
