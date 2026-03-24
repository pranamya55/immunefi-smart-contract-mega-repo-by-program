"""
Get all transaction from blocks
"""

from web3 import Web3
from moneyonchain.networks import network_manager
from moneyonchain.chain import block_filtered_transactions
import csv
import time
from collections import OrderedDict
import datetime


connection_network = 'rskMainnetLocal2'
config_network = 'mocMainnet2'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)

LOCAL_TIMEZONE = datetime.datetime.now().astimezone().tzinfo

from_block = 4142338  # from block start, the block creation of moc contract
to_block = 4152338 #4232338  # block end or 0 to last block
block_steps = 10000
last_block_number = int(network_manager.block_number)
hours_delta = 0
l_accounts = ['0xd554a563adfd9198782add9ad7554c6ffe87ef09']
l_to_contracts = []

if to_block <= 0:
    to_block = last_block_number  # last block number in the node

current_block = from_block

l_transactions = list()

print("Starting Scan Blocks From Block: {0} To Block: {1} ...".format(from_block, to_block))

start_time = time.time()
while current_block <= to_block:

    step_end = current_block + block_steps
    if step_end > to_block:
        step_end = to_block

    print("Scanning blocks steps from {0} to {1}".format(current_block, step_end))

    for n_block in range(current_block, step_end):

        fil_txs = block_filtered_transactions(n_block, full_transactions=True, filter_tx=l_accounts)
        receipts = fil_txs["receipts"]

        if receipts:
            for tx_rcp in receipts:
                d_tx = OrderedDict()
                d_tx["hash"] = str(tx_rcp.txid)
                d_tx["blockNumber"] = tx_rcp.block_number
                d_tx["from"] = tx_rcp.sender
                d_tx["to"] = tx_rcp.receiver
                d_tx["value"] = str(tx_rcp.value)
                d_tx["gas"] = tx_rcp.gas_limit
                d_tx["gasPrice"] = str(tx_rcp.gas_price)
                d_tx["input"] = tx_rcp.input
                d_tx["receipt"] = True
                d_tx["processed"] = False
                d_tx["gas_used"] = tx_rcp.gas_used
                d_tx["confirmations"] = tx_rcp.confirmations
                d_tx["timestamp"] = datetime.datetime.fromtimestamp(tx_rcp.timestamp, LOCAL_TIMEZONE)
                d_tx["logs"] = tx_rcp.logs
                d_tx["status"] = tx_rcp.status
                d_tx["createdAt"] = datetime.datetime.fromtimestamp(tx_rcp.timestamp, LOCAL_TIMEZONE)
                d_tx["lastUpdatedAt"] = datetime.datetime.now()
                d_tx["fee"] = Web3.fromWei(d_tx['gas_used'] * int(d_tx['gasPrice']), 'ether')

                if d_tx["from"].lower() in l_accounts:
                    d_tx["type"] = 'SENT'
                elif d_tx["to"].lower() in l_accounts:
                    d_tx["type"] = 'RECEIVED'
                else:
                    d_tx["type"] = 'N/A'

                # filter to address, if is empty continue...
                if l_to_contracts:
                    if d_tx['to'] not in l_to_contracts:
                        continue

                l_transactions.append(d_tx)

                # print
                print("Hash: {7} Block: {0} From: {1} To: {2} Gas used: {3} Cost: {4} Type: {5} Date: {6}".format(
                    d_tx["blockNumber"],
                    d_tx["from"],
                    d_tx["to"],
                    d_tx["gas_used"],
                    d_tx["fee"],
                    d_tx["type"],
                    d_tx["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                    d_tx["hash"][:7] + '...' + d_tx["hash"][-7:],
                ))

    # Adjust current blocks to the next step
    current_block = current_block + block_steps


columns = ['Nº', 'Block Nº', 'Tx', 'From', 'To', 'Gas Used', 'Gas Price', 'Cost', 'Type', 'Timestamp']
path_file = '{0}_Transactions_{1}_{2}.csv'.format(config_network, from_block, to_block)
with open(path_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(columns)

    count = 0
    for transaction_d in l_transactions:

        count += 1
        row = [count,
               transaction_d['blockNumber'],
               transaction_d["hash"],
               transaction_d['from'],
               transaction_d['to'],
               transaction_d['gas_used'],
               transaction_d['gasPrice'],
               format(transaction_d['fee'], '.18f'),
               transaction_d['type'],
               transaction_d["timestamp"].strftime("%Y-%m-%d %H:%M:%S")]
        writer.writerow(row)

duration = time.time() - start_time
print("Scanning Blocks done! Succesfull!! Done in {0} seconds".format(duration))
