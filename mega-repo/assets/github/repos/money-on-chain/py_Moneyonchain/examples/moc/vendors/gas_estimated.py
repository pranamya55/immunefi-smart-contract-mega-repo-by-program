"""
To run this script need private key, run this scripts with:

user> export ACCOUNT_PK_SECRET=PK
user> python ./mint_bpro.py

Where replace with your PK, and also you need to have funds in this account
"""


from decimal import Decimal
from moneyonchain.networks import network_manager
from moneyonchain.moc_vendors import VENDORSMoC

connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'

# Connect to network
network_manager.connect(
    connection_network=connection_network,
    config_network=config_network)


moc_main = VENDORSMoC(network_manager).from_abi()

amount_want_to_mint = Decimal(0.0001)

gas_estimated = moc_main.mint_bpro_gas_estimated(amount_want_to_mint)
print("To mint BPRO gas estimation: {0}".format(gas_estimated))

gas_estimated = moc_main.mint_doc_gas_estimated(amount_want_to_mint)
print("To mint DOC gas estimation: {0}".format(gas_estimated))

gas_estimated = moc_main.mint_bprox_gas_estimated(amount_want_to_mint)
print("To mint BTCX gas estimation: {0}".format(gas_estimated))

# finally disconnect from network
network_manager.disconnect()
