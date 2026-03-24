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

from web3 import Web3
from decimal import Decimal
from moneyonchain.networks import network_manager
from moneyonchain.tokens import MoCToken

connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnetAlpha'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_vendors_address = network_manager.options['networks'][config_network]['addresses']['MoCVendors']
moc_address = network_manager.options['networks'][config_network]['addresses']['MoC']
#account_address = '0xbB3552267f52B0F06BefBD1bd587E3dBFc7d06BD'
account_address = '0xDda74880D638451e6D2c8D3fC19987526A7Af730'
#account_address = '0xCD8a1C9aCC980Ae031456573e34Dc05CD7dAE6e3'
#account_address = '0xf69287F5Ca3cC3C6d3981f2412109110cB8af076'
#account_address = '0xC61820bFB8F87391d62Cd3976dDc1d35e0cf7128'

#moc_token_address = '0x9aC7Fe28967b30e3a4E6E03286D715B42B453d10'
#moc_token_address = '0x45A97b54021A3F99827641AFE1bFae574431E6ab'
moc_token_address = '0x0399c7F7B37E21cB9dAE04Fb57E24c68ed0B4635'
amount_allow = 0

moc_token = MoCToken(network_manager, contract_address=moc_token_address).from_abi()

print("MoC Token address: {0}".format(moc_token_address))
print("Account: {0}".format(account_address))
print("Balance: {0} {1}".format(moc_token.balance_of(account_address), moc_token.symbol()))
print("Allowance: {0} {1}".format(moc_token.allowance(account_address, moc_address), moc_token.symbol()))

if amount_allow > 0:
    print("Allowing ... {0} MOC".format(amount_allow))
    moc_token.approve(moc_address, amount_allow)

# finally disconnect from network
network_manager.disconnect()
