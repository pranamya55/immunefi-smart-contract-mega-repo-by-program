"""
"""

from web3 import Web3

from moneyonchain.networks import network_manager, web3
from moneyonchain.transaction import TransactionReceipt

connection_network = 'rskTestnetLocal'
config_network = 'mocTestnetAlpha'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

tx_id = '0x14b487543f60dc534a83204965466d3665cebe5745ee5c5cebb00b65a9b49ee4'
tx_receipt = web3.eth.getTransactionReceipt(tx_id)
print(tx_receipt)

tx_receipt = TransactionReceipt(tx_id)
tx_receipt.info()

# tx_id = '0x73a0ce47ab64a31e542670578c73dbfb8f21c1c59a176bd462918db63566f42a'
# tx_receipt = TransactionReceiptBase(tx_id, trace_enabled=True)
# print(tx_receipt.status)
# #tx_receipt.info()
# print(tx_receipt.revert_msg)


tx_hash = tx_receipt.txid
print(tx_hash)

print(tx_receipt.events)
print(tx_receipt.logs)
print(tx_receipt.sender)
print(tx_receipt.receiver)
print(tx_receipt.fn_name)
print(tx_receipt.contract_name)
print(tx_receipt.value)
print(tx_receipt.gas_price)
print(tx_receipt.confirmations)



# finally disconnect from network
network_manager.disconnect()
