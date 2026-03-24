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

connection_network = 'bscTestnetPrivate'
config_network = 'bnbTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_state = MoCState(network_manager).from_abi()
moc = MoC(network_manager).from_abi()
moc_inrate = MoCInrate(network_manager).from_abi()
moc_settlement = MoCSettlement(network_manager).from_abi()
multicall = Multicall2(network_manager).from_abi()

BUCKET_X2 = moc_state.bucket_x2()
BUCKET_C0 = moc_state.bucket_c0()


d_moc_state = OrderedDict()
moc_state_address = moc_state.address()
moc_address = moc.address()
moc_inrate_address = moc_inrate.address()
moc_settlement_address = moc_settlement.address()

list_aggregate = list()
list_aggregate.append((moc_state_address, moc_state.sc.getBitcoinPrice, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 0
list_aggregate.append((moc_state_address, moc_state.sc.getMoCPrice, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 1
list_aggregate.append((moc_state_address, moc_state.sc.absoluteMaxBPro, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 2
list_aggregate.append((moc_state_address, moc_state.sc.maxBProx, [BUCKET_X2], lambda x: str(Web3.fromWei(x, 'ether'))))  # 3
list_aggregate.append((moc_state_address, moc_state.sc.absoluteMaxDoc, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 4
list_aggregate.append((moc_state_address, moc_state.sc.freeDoc, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 5
list_aggregate.append((moc_state_address, moc_state.sc.leverage, [BUCKET_C0], lambda x: str(Web3.fromWei(x, 'ether'))))   # 6
list_aggregate.append((moc_state_address, moc_state.sc.cobj, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 7
list_aggregate.append((moc_state_address, moc_state.sc.leverage, [BUCKET_X2], lambda x: str(Web3.fromWei(x, 'ether'))))  # 8
list_aggregate.append((moc_state_address, moc_state.sc.rbtcInSystem, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 9
list_aggregate.append((moc_state_address, moc_state.sc.getBitcoinMovingAverage, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 10
list_aggregate.append((moc_state_address, moc_state.sc.getInrateBag, [BUCKET_C0], lambda x: str(Web3.fromWei(x, 'ether'))))  # 11
list_aggregate.append((moc_state_address, moc_state.sc.getBucketNBTC, [BUCKET_C0], lambda x: str(Web3.fromWei(x, 'ether'))))  # 12
list_aggregate.append((moc_state_address, moc_state.sc.getBucketNDoc, [BUCKET_C0], lambda x: str(Web3.fromWei(x, 'ether'))))  # 13
list_aggregate.append((moc_state_address, moc_state.sc.getBucketNBPro, [BUCKET_C0], lambda x: str(Web3.fromWei(x, 'ether'))))  # 14
list_aggregate.append((moc_state_address, moc_state.sc.getBucketNBTC, [BUCKET_X2], lambda x: str(Web3.fromWei(x, 'ether'))))  # 15
list_aggregate.append((moc_state_address, moc_state.sc.getBucketNDoc, [BUCKET_X2], lambda x: str(Web3.fromWei(x, 'ether'))))  # 16
list_aggregate.append((moc_state_address, moc_state.sc.getBucketNBPro, [BUCKET_X2], lambda x: str(Web3.fromWei(x, 'ether'))))  # 17
list_aggregate.append((moc_state_address, moc_state.sc.globalCoverage, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 18
list_aggregate.append((moc_address, moc.sc.getReservePrecision, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 19
list_aggregate.append((moc_address, moc.sc.getMocPrecision, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 20
list_aggregate.append((moc_state_address, moc_state.sc.coverage, [BUCKET_X2], lambda x: str(Web3.fromWei(x, 'ether'))))  # 21
list_aggregate.append((moc_state_address, moc_state.sc.bproTecPrice, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 22
list_aggregate.append((moc_state_address, moc_state.sc.bproUsdPrice, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 23
list_aggregate.append((moc_state_address, moc_state.sc.bproSpotDiscountRate, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 24
list_aggregate.append((moc_state_address, moc_state.sc.maxBProWithDiscount, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 25
list_aggregate.append((moc_state_address, moc_state.sc.bproDiscountPrice, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 26
list_aggregate.append((moc_state_address, moc_state.sc.bucketBProTecPrice, [BUCKET_X2], lambda x: str(Web3.fromWei(x, 'ether'))))  # 27
list_aggregate.append((moc_state_address, moc_state.sc.bproxBProPrice, [BUCKET_X2], lambda x: str(Web3.fromWei(x, 'ether'))))  # 28
list_aggregate.append((moc_inrate_address, moc_inrate.sc.spotInrate, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 29
list_aggregate.append((moc_inrate_address, moc_inrate.sc.MINT_BPRO_FEES_RBTC, [], lambda x: str(x)))   # 30
list_aggregate.append((moc_inrate_address, moc_inrate.sc.REDEEM_BPRO_FEES_RBTC, [], lambda x: str(x)))  # 31
list_aggregate.append((moc_inrate_address, moc_inrate.sc.MINT_DOC_FEES_RBTC, [], lambda x: str(x)))  # 32
list_aggregate.append((moc_inrate_address, moc_inrate.sc.REDEEM_DOC_FEES_RBTC, [], lambda x: str(x)))  # 33
list_aggregate.append((moc_inrate_address, moc_inrate.sc.MINT_BTCX_FEES_RBTC, [], lambda x: str(x)))  # 34
list_aggregate.append((moc_inrate_address, moc_inrate.sc.REDEEM_BTCX_FEES_RBTC, [], lambda x: str(x)))  # 35
list_aggregate.append((moc_inrate_address, moc_inrate.sc.MINT_BPRO_FEES_MOC, [], lambda x: str(x)))  # 36
list_aggregate.append((moc_inrate_address, moc_inrate.sc.REDEEM_BPRO_FEES_MOC, [], lambda x: str(x)))  # 37
list_aggregate.append((moc_inrate_address, moc_inrate.sc.MINT_DOC_FEES_MOC, [], lambda x: str(x)))  # 38
list_aggregate.append((moc_inrate_address, moc_inrate.sc.REDEEM_DOC_FEES_MOC, [], lambda x: str(x)))  # 39
list_aggregate.append((moc_inrate_address, moc_inrate.sc.MINT_BTCX_FEES_MOC, [], lambda x: str(x)))  # 40
list_aggregate.append((moc_inrate_address, moc_inrate.sc.REDEEM_BTCX_FEES_MOC, [], lambda x: str(x)))  # 41
list_aggregate.append((moc_state_address, moc_state.sc.dayBlockSpan, [], lambda x: x))  # 42
list_aggregate.append((moc_settlement_address, moc_settlement.sc.getBlockSpan, [], lambda x: x))  # 43
list_aggregate.append((moc_state_address, moc_state.sc.blocksToSettlement, [], lambda x: x))  # 44
list_aggregate.append((moc_state_address, moc_state.sc.state, [], lambda x: x))  # 45
list_aggregate.append((moc_address, moc.sc.paused, [], lambda x: x))  # 46
list_aggregate.append((moc_state_address, moc_state.sc.getLiquidationEnabled, [], lambda x: x))  # 47
list_aggregate.append((moc_state_address, moc_state.sc.getProtected, [], lambda x: str(Web3.fromWei(x, 'ether'))))  # 48
list_aggregate.append((moc_state_address, moc_state.sc.getMoCToken, [], lambda x: str(x)))  # 49
list_aggregate.append((moc_state_address, moc_state.sc.getMoCPriceProvider, [], lambda x: str(x)))  # 50
list_aggregate.append((moc_state_address, moc_state.sc.getBtcPriceProvider, [], lambda x: str(x)))  # 51
list_aggregate.append((moc_state_address, moc_state.sc.getMoCVendors, [], lambda x: str(x)))  # 52

results = multicall.aggregate_multiple(list_aggregate)

block_number = results[0]

d_moc_state["blockHeight"] = block_number
d_moc_state["bitcoinPrice"] = results[1][0]
d_moc_state["mocPrice"] = results[1][1]
d_moc_state["bproAvailableToRedeem"] = results[1][2]
d_moc_state["bprox2AvailableToMint"] = results[1][3]
d_moc_state["docAvailableToMint"] = results[1][4]
d_moc_state["docAvailableToRedeem"] = results[1][5]
d_moc_state["b0Leverage"] = results[1][6]
d_moc_state["b0TargetCoverage"] = results[1][7]
d_moc_state["x2Leverage"] = results[1][8]
d_moc_state["totalBTCAmount"] = results[1][9]
d_moc_state["bitcoinMovingAverage"] = results[1][10]
d_moc_state["b0BTCInrateBag"] = results[1][11]
d_moc_state["b0BTCAmount"] = results[1][12]
d_moc_state["b0DocAmount"] = results[1][13]
d_moc_state["b0BproAmount"] = results[1][14]
d_moc_state["x2BTCAmount"] = results[1][15]
d_moc_state["x2DocAmount"] = results[1][16]
d_moc_state["x2BproAmount"] = results[1][17]
d_moc_state["globalCoverage"] = results[1][18]
d_moc_state["reservePrecision"] = results[1][19]
d_moc_state["mocPrecision"] = results[1][20]
d_moc_state["x2Coverage"] = results[1][21]
d_moc_state["bproPriceInRbtc"] = results[1][22]
d_moc_state["bproPriceInUsd"] = results[1][23]
d_moc_state["bproDiscountRate"] = results[1][24]
d_moc_state["maxBproWithDiscount"] = results[1][25]
d_moc_state["bproDiscountPrice"] = results[1][26]
d_moc_state["bprox2PriceInRbtc"] = results[1][27]
d_moc_state["bprox2PriceInBpro"] = results[1][28]
d_moc_state["spotInrate"] = results[1][29]

# Start: Commission rates by transaction types
commission_rates = dict()
commission_rates["MINT_BPRO_FEES_RBTC"] = results[1][30]
commission_rates["REDEEM_BPRO_FEES_RBTC"] = results[1][31]
commission_rates["MINT_DOC_FEES_RBTC"] = results[1][32]
commission_rates["REDEEM_DOC_FEES_RBTC"] = results[1][33]
commission_rates["MINT_BTCX_FEES_RBTC"] = results[1][34]
commission_rates["REDEEM_BTCX_FEES_RBTC"] = results[1][35]
commission_rates["MINT_BPRO_FEES_MOC"] = results[1][36]
commission_rates["REDEEM_BPRO_FEES_MOC"] = results[1][37]
commission_rates["MINT_DOC_FEES_MOC"] = results[1][38]
commission_rates["REDEEM_DOC_FEES_MOC"] = results[1][39]
commission_rates["MINT_BTCX_FEES_MOC"] = results[1][40]
commission_rates["REDEEM_BTCX_FEES_MOC"] = results[1][41]

d_moc_state["commissionRates"] = commission_rates
# End: Commission rates by transaction types

# d_moc_state["bprox2PriceInUsd"] = str(
#     int(d_moc_state["bprox2PriceInRbtc"]) * int(
#         d_moc_state["bitcoinPrice"]) / int(
#         d_moc_state["reservePrecision"]))

d_moc_state["dayBlockSpan"] = results[1][42]
d_moc_state["blockSpan"] = results[1][43]
d_moc_state["blocksToSettlement"] = results[1][44]
d_moc_state["state"] = results[1][45]
d_moc_state["lastPriceUpdateHeight"] = 0
d_moc_state["paused"] = results[1][46]
d_moc_state["liquidationEnabled"] = results[1][47]
d_moc_state["protected"] = results[1][48]
d_moc_state["getMoCToken"] = results[1][49]
d_moc_state["getMoCPriceProvider"] = results[1][50]
d_moc_state["getBtcPriceProvider"] = results[1][51]
d_moc_state["getMoCVendors"] = results[1][52]


pp.pprint(d_moc_state)

# finally disconnect from network
network_manager.disconnect()
