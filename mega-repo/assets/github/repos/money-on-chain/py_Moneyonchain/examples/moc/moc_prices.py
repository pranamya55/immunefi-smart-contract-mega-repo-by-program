"""
 brownie networks add BSCNetwork bscTestnet host=https://data-seed-prebsc-1-s1.binance.org:8545/ chainid=97 explorer=https://blockscout.com/rsk/mainnet/api
"""

from collections import OrderedDict
import pprint
from web3 import Web3

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoCState, MoC, MoCInrate, MoCSettlement
from moneyonchain.multicall import Multicall2


pp = pprint.PrettyPrinter(indent=4)

connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_state = MoCState(network_manager).from_abi()
moc = MoC(network_manager).from_abi()
moc_inrate = MoCInrate(network_manager).from_abi()
moc_settlement = MoCSettlement(network_manager).from_abi()
multicall = Multicall2(network_manager).from_abi()

BUCKET_X2 = moc_state.bucket_x2()
BUCKET_C0 = moc_state.bucket_c0()


d_price = OrderedDict()
moc_state_address = moc_state.address()
moc_address = moc.address()
moc_inrate_address = moc_inrate.address()
moc_settlement_address = moc_settlement.address()

list_aggregate = list()


list_aggregate.append((moc_state_address, moc_state.sc.getBitcoinPrice, [], lambda x: str(x)))
list_aggregate.append((moc_state_address, moc_state.sc.bproTecPrice, [], lambda x: str(x)))
list_aggregate.append((moc_state_address, moc_state.sc.bproUsdPrice, [], lambda x: str(x)))
list_aggregate.append((moc_state_address, moc_state.sc.bproDiscountPrice, [], lambda x: str(x)))
list_aggregate.append((moc_state_address, moc_state.sc.bucketBProTecPrice, [BUCKET_X2], lambda x: str(x)))
list_aggregate.append((moc_state_address, moc_state.sc.bproxBProPrice, [BUCKET_X2], lambda x: str(x)))
list_aggregate.append((moc_address, moc.sc.getReservePrecision, [], lambda x: str(x)))
list_aggregate.append((moc_state_address, moc_state.sc.getMoCPrice, [], lambda x: str(x)))


results = multicall.aggregate_multiple(list_aggregate, block_identifier=2564639)

print(results)

block_number = results[0]

d_price["blockHeight"] = block_number
d_price["bitcoinPrice"] = results[1][0]
d_price["bproPriceInRbtc"] = results[1][1]
d_price["bproPriceInUsd"] = results[1][2]
d_price["bproDiscountPrice"] = results[1][3]
d_price["bprox2PriceInRbtc"] = results[1][4]
d_price["bprox2PriceInBpro"] = results[1][5]
d_price["reservePrecision"] = results[1][6]
d_price["bprox2PriceInUsd"] = str(
    int(d_price["bprox2PriceInRbtc"]) * int(d_price["bitcoinPrice"]) / int(
        d_price["reservePrecision"]))
d_price["mocPrice"] = results[1][7]

pp.pprint(d_price)

# errors
pp.pprint(results[2])

# finally disconnect from network
network_manager.disconnect()
