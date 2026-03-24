"""

If is the first time to py_Moneyonchain we need brownie framework installed

`pip install eth-brownie==1.12.2`

and to install connection nodes required to connect, also run :

```
console> brownie networks add RskNetwork rskTestnetPublic host=https://public-node.testnet.rsk.co chainid=31 explorer=https://blockscout.com/rsk/mainnet/api
console> brownie networks add RskNetwork rskTestnetLocal host=http://localhost:4444 chainid=31 explorer=https://blockscout.com/rsk/mainnet/api
console> brownie networks add RskNetwork rskMainnetPublic host=https://public-node.rsk.co chainid=30 explorer=https://blockscout.com/rsk/mainnet/api
console> brownie networks add RskNetwork rskMainnetLocal host=http://localhost:4444 chainid=30 explorer=https://blockscout.com/rsk/mainnet/api
```

"""

import datetime
from tabulate import tabulate
import time
from web3 import Web3
import csv

from moneyonchain.networks import network_manager
from moneyonchain.networks import chain
from moneyonchain.moc import MoCExchangeRiskProMint, MoCExchangeRiskProRedeem, MoCExchangeRiskProxMint, \
    MoCExchangeRiskProxRedeem, MoCExchangeStableTokenMint, MoCExchangeStableTokenRedeem, \
    MoCExchangeFreeStableTokenRedeem
from moneyonchain.rdoc import RDOCMoCState
from moneyonchain.utils import filter_transactions


connection_network = 'rskMainnetPublic'
config_network = 'rdocMainnet'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)


from_block = 3086506  # can be manually setting
to_block = 3086968  # can be manually setting

current_block = from_block

start_time = time.time()

filter_addresses = [str.lower('0xe5e54B50B8Fa25c5715dd60CBF7aaA575E740EE3')]

list_transactions = list()
while current_block <= to_block:

    d_block = chain.get_block(current_block)
    all_transactions = d_block['transactions']

    # filtered transactions
    fil_transactions, d_fil_transactions = filter_transactions(all_transactions, filter_addresses)

    if fil_transactions:
        for fil_tx in fil_transactions:
            list_transactions.append(Web3.toHex(fil_tx['hash']))

    print("Processed block: {0}".format(current_block))

    current_block += 1

# list_transactions = [
#     '0x8cda84f523b88794c1d480375be0d770bd778adf0ddb00ecd8e5dfc6e2bf54fd',
#     '0x24825537378ad9c331e2281bb266f71a2550843bdd40d0e1671e3848f00ac4cd',
#     '0x5337f124a8aeae23d1f29e844d73dce6e391176ff806018c00bea9d3c11ea890',
#     '0x295af1b05ed8b524faab61af8a3862b547e4a176ed10028a4fd43ef76ce84a43',
#     '0xc1212c72938c3dd0c18c4d91e03c78574f73a340bc71f3dcd32e09c600b0aa1e',
#     '0x80253cd80bd7211e9fc2247aa612786d900ef89fb1b83752dce73212b1bfe5c2',
#     '0xaa03295c76f3a36ba18095b3a70c3ad099986ef730aff788caf23e59145ec6e4',
#     '0x6381fe289924d2402a9392b02d08381553c6ddadc149a7ad746f1f45badf25fa',
#     '0x977106d00c7aaf855478abe78f9e7ccbed11cc427d310dbe299896f5e279652b',
#     '0x28055bdc3ceb73caaa90cd931c982e3d8847c102e96bcc5dad193c1b2d8380b1',
#     '0x31ed115004625d43ce5671ef7c9539b09c7dd85c1083d96c5a067cf882d021fa',
#     '0xcd6047940ce563aa8decc4f4122a3addd5488c62bcefd8976c7bdc6e7050ae4f',
#     '0x0a65e3e03a0c973daa9d2fb4cc8a9a90f694ac820e67f1aebc96f56d9794d3c2',
#     '0xfff76f39f992f6ca33cd167d34141005d86914e4bdfbeb54a0113756d1b18dd6',
#     '0x78ece9329bc57b70a419482769c802daa4b0c501384886143cc6209ad4fef553'
# ]

moc_state = RDOCMoCState(network_manager).from_abi()

l_actions = list()
for tx_id in list_transactions:
    tx_receipt = chain.get_transaction(tx_id)

    d_event = dict()
    d_event['transactionHash'] = tx_receipt.txid
    d_event['blockNumber'] = tx_receipt.block_number
    d_event['timestamp'] = datetime.datetime.fromtimestamp(tx_receipt.timestamp)
    d_event['reserves'] = moc_state.rbtc_in_system(block_identifier=tx_receipt.block_number)

    tx_events = tx_receipt.events
    if 'RiskProMint' in tx_events:
        for tx_event in tx_events['RiskProMint']:
            event = MoCExchangeRiskProMint(tx_event, tx_receipt=tx_receipt)
            d_event['function'] = 'RiskProMint'
            d_event['account'] = event.formatted()['account']
            d_event['amount'] = event.formatted()['amount']
            d_event['reservePrice'] = event.formatted()['reservePrice']
            d_event['amount_usd'] = d_event['amount'] * d_event['reservePrice']
            l_actions.append(d_event)
    elif 'RiskProRedeem' in tx_events:
        for tx_event in tx_events['RiskProRedeem']:
            event = MoCExchangeRiskProRedeem(tx_event, tx_receipt=tx_receipt)
            d_event['function'] = 'MoCExchangeRiskProRedeem'
            d_event['account'] = event.formatted()['account']
            d_event['amount'] = event.formatted()['amount']
            d_event['reservePrice'] = event.formatted()['reservePrice']
            d_event['amount_usd'] = d_event['amount'] * d_event['reservePrice']
            l_actions.append(d_event)
    elif 'RiskProxMint' in tx_events:
        for tx_event in tx_events['RiskProxMint']:
            event = MoCExchangeRiskProxMint(tx_event, tx_receipt=tx_receipt)
            d_event['function'] = 'MoCExchangeRiskProxMint'
            d_event['account'] = event.formatted()['account']
            d_event['amount'] = event.formatted()['amount']
            d_event['reservePrice'] = event.formatted()['reservePrice']
            d_event['amount_usd'] = d_event['amount'] * d_event['reservePrice']
            l_actions.append(d_event)
    elif 'RiskProxRedeem' in tx_events:
        for tx_event in tx_events['RiskProxRedeem']:
            event = MoCExchangeRiskProxRedeem(tx_event, tx_receipt=tx_receipt)
            d_event['function'] = 'RiskProxRedeem'
            d_event['account'] = event.formatted()['account']
            d_event['amount'] = event.formatted()['amount']
            d_event['reservePrice'] = event.formatted()['reservePrice']
            d_event['amount_usd'] = d_event['amount'] * d_event['reservePrice']
            l_actions.append(d_event)
    elif 'StableTokenMint' in tx_events:
        for tx_event in tx_events['StableTokenMint']:
            event = MoCExchangeStableTokenMint(tx_event, tx_receipt=tx_receipt)
            d_event['function'] = 'StableTokenMint'
            d_event['account'] = event.formatted()['account']
            d_event['amount'] = event.formatted()['amount']
            d_event['reservePrice'] = event.formatted()['reservePrice']
            d_event['amount_usd'] = d_event['amount'] * d_event['reservePrice']
            l_actions.append(d_event)
    elif 'StableTokenRedeem' in tx_events:
        for tx_event in tx_events['StableTokenRedeem']:
            event = MoCExchangeStableTokenRedeem(tx_event, tx_receipt=tx_receipt)
            d_event['function'] = 'StableTokenRedeem'
            d_event['account'] = event.formatted()['account']
            d_event['amount'] = event.formatted()['amount']
            d_event['reservePrice'] = event.formatted()['reservePrice']
            d_event['amount_usd'] = d_event['amount'] * d_event['reservePrice']
            l_actions.append(d_event)
    elif 'FreeStableTokenRedeem' in tx_events:
        for tx_event in tx_events['FreeStableTokenRedeem']:
            event = MoCExchangeFreeStableTokenRedeem(tx_event, tx_receipt=tx_receipt)
            d_event['function'] = 'FreeStableTokenRedeem'
            d_event['account'] = event.formatted()['account']
            d_event['amount'] = event.formatted()['amount']
            d_event['reservePrice'] = event.formatted()['reservePrice']
            d_event['amount_usd'] = d_event['amount'] * d_event['reservePrice']
            l_actions.append(d_event)


if l_actions:
    columns = ['blockNumber', 'Timestamp', 'Account', 'Function', 'Amount', 'Amount USD', 'Reserve price', 'Reserves System']
    path_file = '{0}_inv_MCS001_{1}_{2}.csv'.format(config_network, from_block, to_block)
    with open(path_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(columns)

        count = 0
        for action in l_actions:
            count += 1
            row = [ action['blockNumber'],
                    action['timestamp'],
                    action['account'],
                    action['function'],
                    action['amount'],
                    action['amount_usd'],
                    action['reservePrice'],
                    action['reserves'],
                  ]
            writer.writerow(row)


display_table = []
titles = ['blockNumber', 'Timestamp', 'Account', 'Function', 'Amount', 'Amount USD', 'Reserve price', 'Reserves System']

for action in l_actions:
    display_table.append([
        action['blockNumber'],
        action['timestamp'],
        action['account'],
        action['function'],
        action['amount'],
        action['amount_usd'],
        action['reservePrice'],
        action['reserves'],
    ])

print(tabulate(display_table, headers=titles, tablefmt="pipe"))

# finally disconnect from network
network_manager.disconnect()


duration = time.time() - start_time
print("Getting historic data done! Succesfull!! Done in {0} seconds".format(duration))
