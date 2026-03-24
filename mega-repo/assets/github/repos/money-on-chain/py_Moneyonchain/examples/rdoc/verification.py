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

This script list all of the proxy and implementation addresses of the contracts in the network.

Output:

Connecting to rdocMainnet...
Connected: True

| Nº     | Contract                      | Address Proxy                  | Address Implementation           |
| :---:  | :---------------------------- | ----------------------------   | -------------------------------- |
| 1 | MOC  | 0xCfF3fcaeC2352C672C38d77cb1a064B7D50ce7e1  | 0x874056dE3941F1aa208188E91a86fDFC498Ac7a2 |
| 2 | MoCConnector  | 0xA0e2554E525B34FD186C2C356C93d563541b02C0  | 0x6b3f320a7944189607d5FB2360B8D353880d8bD3 |
| 3 | MoCState  | 0x541F68a796Fe5ae3A381d2Aa5a50b975632e40A6  | 0x6d155B3A6A391532f648153E444001746264968c |
| 4 | MoCConverter  | 0x94f6680201e5FBCA94fB8569adFD8C1EE7Cb061C  | 0x2E73EAb8fAE69B022B3c41719Ee6386D76Ffafd5 |
| 5 | MoCSettlement  | 0xb8a6beBa78c3E73f6A66DDacFaEB240ae22Ca709  | 0xFED9C20050644EeDb5dFabD64d890a8AD43eDC2c |
| 6 | MoCExchange  | 0x9497d2AEcd0757Dd4fcb4d5F2131293570FaD305  | 0xD5F8bcb6440c03305eB76473103f6Da6B9328721 |
| 7 | MoCInrate  | 0x1DaB07c4FD07d6eE1359a5198ACa2DEe64F371f3  | 0xB637A4ff35CDBE27C9c061F0FA7e0F18e1D59bAA |
| 8 | MoCBurnout  | 0x89fBF64ea00123F03b41f60eC23Cf1b6C6E382a8  | 0x40bc17998288E44F6A4CB9B5FBCc4bec4b499A1d |
| 9 | MoCBProxManager  | 0x07Cd11fC4c4eC0BdBdC2Ec495f66A69bba32e7e7  | 0x0175ec99026D177F2B69E53B951b2E7e27b4f4b4 |
| 10 | RIFDoC  |   | 0x2d919F19D4892381D58edeBeca66D5642Cef1a1f |
| 11 | RIFPro  |   | 0xf4d27c56595Ed59B66cC7F03CFF5193e4bd74a61 |
| 12 | MoCMedianizer  |   | 0x504EfCadFB020d6bBaeC8a5c5BB21453719d0E00 |


"""

from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoC, \
    RDOCMoCConverter, \
    RDOCMoCSettlement, \
    RDOCMoCExchange, \
    RDOCMoCInrate, \
    RDOCMoCBurnout, \
    RDOCMoCBProxManager, \
    RDOCMoCState, \
    RDOCMoCConnector
from moneyonchain.medianizer import RDOCMoCMedianizer
from moneyonchain.tokens import RIFDoC, RIFPro


connection_network = 'rskMainnetPublic'
config_network = 'rdocMainnet'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_main = RDOCMoC(network_manager).from_abi()
addresses = moc_main.connector_addresses()

count = 0
lines = list()

md_header = '''
| Nº     | Contract                      | Address Proxy                  | Address Implementation           |
| :---:  | :---------------------------- | ----------------------------   | -------------------------------- |
'''

# MOC
count += 1
line = '| {0} | {1}  | {2}  | {3} |'.format(count, 'MOC', addresses['MoC'], moc_main.implementation())
lines.append(line)

# MoCConnector
count += 1
contract = RDOCMoCConnector(network_manager).from_abi()
line = '| {0} | {1}  | {2}  | {3} |'.format(count, 'MoCConnector', contract.address(),
                                            contract.implementation())
lines.append(line)


# MoCState
count += 1
contract = RDOCMoCState(network_manager).from_abi()
line = '| {0} | {1}  | {2}  | {3} |'.format(count, 'MoCState', addresses['MoCState'],
                                            contract.implementation())
lines.append(line)

# MoCConverter
contract = RDOCMoCConverter(network_manager).from_abi()
count += 1
line = '| {0} | {1}  | {2}  | {3} |'.format(count, 'MoCConverter', addresses['MoCConverter'],
                                            contract.implementation())
lines.append(line)

# MoCSettlement
contract = RDOCMoCSettlement(network_manager).from_abi()
count += 1
line = '| {0} | {1}  | {2}  | {3} |'.format(count, 'MoCSettlement', addresses['MoCSettlement'],
                                            contract.implementation())
lines.append(line)

# MoCExchange
contract = RDOCMoCExchange(network_manager).from_abi()
count += 1
line = '| {0} | {1}  | {2}  | {3} |'.format(count, 'MoCExchange', addresses['MoCExchange'],
                                            contract.implementation()) # block_identifier=1757099
lines.append(line)

# MoCInrate
contract = RDOCMoCInrate(network_manager).from_abi()
count += 1
line = '| {0} | {1}  | {2}  | {3} |'.format(count, 'MoCInrate', addresses['MoCInrate'],
                                            contract.implementation())
lines.append(line)


# MoCBurnout
contract = RDOCMoCBurnout(network_manager).from_abi()
count += 1
line = '| {0} | {1}  | {2}  | {3} |'.format(count, 'MoCBurnout', addresses['MoCBurnout'],
                                            contract.implementation())
lines.append(line)

# MoCBProxManager
contract = RDOCMoCBProxManager(network_manager).from_abi()
count += 1
line = '| {0} | {1}  | {2}  | {3} |'.format(count, 'MoCBProxManager', addresses['MoCBProxManager'],
                                            contract.implementation())
lines.append(line)

# RIFDoC
contract = RIFDoC(network_manager).from_abi()
count += 1
line = '| {0} | {1}  | {2}  | {3} |'.format(count, 'RIFDoC', '',
                                            contract.address())
lines.append(line)


# RIFPro
contract = RIFPro(network_manager).from_abi()
count += 1
line = '| {0} | {1}  | {2}  | {3} |'.format(count, 'RIFPro', '',
                                            contract.address())
lines.append(line)


# Oracle
contract = RDOCMoCMedianizer(network_manager).from_abi()
count += 1
line = '| {0} | {1}  | {2}  | {3} |'.format(count, 'MoCMedianizer', '',
                                            contract.address())
lines.append(line)


# finally print
print(md_header)
print('\n'.join(lines))
