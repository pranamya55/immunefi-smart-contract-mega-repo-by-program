"""
To run this script need private key, run this scripts with:

user> export ACCOUNT_PK_SECRET=PK
user> python ./mint_doc.py

Where replace with your PK, and also you need to have funds in this account
"""


from decimal import Decimal
from web3 import Web3

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoC

connection_network = 'bscTestnetPrivate'
config_network = 'bnbTestnet'


# Connect to network
network_manager.connect(
    connection_network=connection_network,
    config_network=config_network)


moc_main = MoC(network_manager).from_abi()

amount_want_to_mint = Decimal(0.001)
vendor_account = Web3.toChecksumAddress('0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3')

print("Please wait to the transaction be mined!...")
tx_receipt = moc_main.mint_doc(amount_want_to_mint, vendor_account=vendor_account)

# finally disconnect from network
network_manager.disconnect()
