"""
To run this script need private key, run this scripts with:

user> export ACCOUNT_PK_SECRET=PK
user> python ./mint_bpro.py

Where replace with your PK, and also you need to have funds in this account
"""


from decimal import Decimal
from moneyonchain.networks import network_manager
from moneyonchain.moc import MoC

connection_network = 'bscTestnetPrivate'
config_network = 'bnbTestnet'

# Connect to network
network_manager.connect(
    connection_network=connection_network,
    config_network=config_network)


moc_main = MoC(network_manager).from_abi()

print("Please wait to the transaction be mined!...")

partial_execution_steps = 1

tx_args = moc_main.tx_arguments(gas_limit=3000000, required_confs=1)

tx_receipt = moc_main.sc.runSettlement(
            partial_execution_steps,
            tx_args)

# finally disconnect from network
network_manager.disconnect()
