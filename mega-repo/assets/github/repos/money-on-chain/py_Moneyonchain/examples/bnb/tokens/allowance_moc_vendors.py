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
user> python ./allowance.py

Where replace with your PK, and also you need to have funds in this account
"""

from moneyonchain.networks import network_manager
from moneyonchain.tokens import MoCToken

connection_network = 'bscTestnetPrivate'
config_network = 'bnbTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_vendors_address = network_manager.options['networks'][config_network]['addresses']['MoCVendors']
moc_address = network_manager.options['networks'][config_network]['addresses']['MoC']
moc_token_address = network_manager.options['networks'][config_network]['addresses']['MoCToken']
account_address = '0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3'
amount_allow = 0

moc_token = MoCToken(network_manager, contract_address=moc_token_address).from_abi()

print("MoC Token address: {0}".format(moc_token_address))
print("Account: {0}".format(account_address))
print("Balance: {0} {1}".format(moc_token.balance_of(account_address), moc_token.symbol()))
print("Allowance: {0} {1}".format(moc_token.allowance(account_address, moc_vendors_address), moc_token.symbol()))

if amount_allow > 0:
    print("Allowing ... {0} MOC".format(amount_allow))
    moc_token.approve(moc_vendors_address, amount_allow)

# finally disconnect from network
network_manager.disconnect()
