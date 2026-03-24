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
user> python ./mint_bpro.py

Where replace with your PK, and also you need to have funds in this account
"""

from web3 import Web3
from decimal import Decimal
from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoC

connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnetAlpha'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_main = RDOCMoC(network_manager).from_abi()

amount_want_to_mint = Decimal(10)

#0xbB3552267f52B0F06BefBD1bd587E3dBFc7d06BD
#0xDda74880D638451e6D2c8D3fC19987526A7Af730
#0xf69287F5Ca3cC3C6d3981f2412109110cB8af076
#0x00adD81c1CfaE0EA2D487490CDE322cb7E77aA5f
vendor_account = Web3.toChecksumAddress('0xDda74880D638451e6D2c8D3fC19987526A7Af730')

print("Please wait to the transaction be mined!...")
tx_receipt = moc_main.mint_bpro(amount_want_to_mint, vendor_account=vendor_account)

# finally disconnect from network
network_manager.disconnect()
