"""
To run this script need private key, run this scripts with:

user> export ACCOUNT_PK_SECRET=PK
user> python ./mint_doc.py

Where replace with your PK, and also you need to have funds in this account
"""

from web3 import Web3
from decimal import Decimal
from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoC

connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnetAlpha'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_main = RDOCMoC(network_manager).from_abi()

amount_want_to_mint = Decimal(1)

vendor_account = Web3.toChecksumAddress('0xDda74880D638451e6D2c8D3fC19987526A7Af730')

# Mint Stable
# This transaction is not async, you have to wait to the transaction is mined
print("Please wait to the transaction be mined!...")
tx_receipt = moc_main.mint_stable(amount_want_to_mint, vendor_account=vendor_account)

# finally disconnect from network
network_manager.disconnect()
