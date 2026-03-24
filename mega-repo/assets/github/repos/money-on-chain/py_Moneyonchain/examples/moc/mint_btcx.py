"""
To run this script need private key, run this scripts with:

user> export ACCOUNT_PK_SECRET=PK
user> python ./mint_btcx.py

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

amount_want_to_mint = Decimal(0.0001)

total_amount, commission_value, interest_value = moc_main.amount_mint_btc2x(amount_want_to_mint)
print("To mint {0} BTC2X need {1} RBTC. Commision: {2} Interest: {3}".format(format(amount_want_to_mint, '.18f'),
                                                                             format(total_amount, '.18f'),
                                                                             format(commission_value, '.18f'),
                                                                             format(interest_value, '.18f')))

# Mint BTC2X
# This transaction is not async, you have to wait to the transaction is mined
print("Please wait to the transaction be mined!...")
tx_receipt = moc_main.mint_btcx(amount_want_to_mint)

# finally disconnect from network
network_manager.disconnect()
