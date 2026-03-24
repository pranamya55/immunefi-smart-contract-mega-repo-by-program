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


To run this script need private key, run this scripts with:

user> export ACCOUNT_PK_SECRET=PK
user> python ./mint_doc.py

Where replace with your PK, and also you need to have funds in this account
"""


from decimal import Decimal
from web3 import Web3
from moneyonchain.networks import network_manager
from moneyonchain.moc import MoC

connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_main = MoC(network_manager).from_abi()

vendor_account = Web3.toChecksumAddress('0xdda74880d638451e6d2c8d3fc19987526a7af730')
amount_want_to_mint = Decimal(0.001)

total_amount, commission_value, markup_value = moc_main.amount_mint_doc(
    amount=amount_want_to_mint,
    vendor_account=vendor_account)

print("To mint {0} RBTC in DOC need {1} RBTC. Commission {2}. Markup {3}".format(
    format(amount_want_to_mint, '.18f'),
    format(total_amount, '.18f'),
    format(commission_value, '.18f'),
    format(markup_value, '.18f')))

tx_args = moc_main.tx_arguments()

re_total_amount = total_amount + (total_amount * Decimal(0.01))

print("Want Amount: {0}".format(int(total_amount * 10 ** 18)))
print("Sent Amount: {0}".format(int(re_total_amount * 10 ** 18)))

tx_args['amount'] = int(re_total_amount * moc_main.precision)
tx_receipt = moc_main.sc.mintDocVendors(
    int(amount_want_to_mint * moc_main.precision),
    vendor_account,
    tx_args)

tx_receipt.info()

# finally disconnect from network
network_manager.disconnect()
