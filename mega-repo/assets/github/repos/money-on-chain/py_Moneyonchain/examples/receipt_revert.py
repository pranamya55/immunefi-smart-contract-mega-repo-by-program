"""
"""

from web3 import Web3

from moneyonchain.networks import network_manager, web3
from moneyonchain.transaction import TransactionReceipt

connection_network = 'rskTestnetLocal2'
config_network = 'mocTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


tx_id = '0x66faf6a7e4034557c26f52c2601f31f59924924f39bbe81faea43d589a9c638c'
tx_receipt = TransactionReceipt(tx_id, trace_enabled=True)
print(tx_receipt.status)
#tx_receipt.info()
print(tx_receipt.revert_msg)

# finally disconnect from network
network_manager.disconnect()
