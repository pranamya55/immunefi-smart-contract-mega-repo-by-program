from moneyonchain.networks import NetworkManager
from moneyonchain.moc import MoCState, MoC
from brownie.convert import to_bytes
from web3 import Web3


connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'

# init network manager
# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager = NetworkManager(
    connection_network=connection_network,
    config_network=config_network)

# run install() if is the first time and you want to install
# networks connection from brownie
# network_manager.install()

# Connect to network
network_manager.connect()

print("Connecting to MoCState")
moc_state = MoCState(network_manager).from_abi()

bucket_x2 = moc_state.bucket_x2()
print(bucket_x2)

bucket_c0 = moc_state.bucket_c0()
print(bucket_c0)

print("Bitcoin Price in USD: {0}".format(moc_state.bitcoin_price()))
print("Bitcoin Moving Average in USD: {0}".format(moc_state.bitcoin_moving_average()))
print("Days to settlement: {0}".format(moc_state.days_to_settlement()))
print("Global Coverage: {0}".format(moc_state.global_coverage()))
print("Bitpro Total Supply: {0}".format(moc_state.bitpro_total_supply()))
print("DOC Total Supply: {0}".format(moc_state.doc_total_supply()))
print("Implementation: {0}".format(moc_state.implementation()))
print("BPro Discount: {0}".format(moc_state.bpro_discount_rate()))
print("BPro Tec Price: {0}".format(moc_state.bpro_tec_price()))

print("State: {0}".format(moc_state.state()))
print("RBTC in System: {0}".format(moc_state.rbtc_in_system()))
print("cobj: {0}".format(moc_state.cobj()))
print("cobjX: {0}".format(moc_state.cobj_X2()))
print("cobjX: {0}".format(moc_state.cobj_X2()))
print("MaxBProX: {0}".format(moc_state.max_bprox(bucket_x2)))
print("MaxBProX BTC Value: {0}".format(moc_state.max_bprox_btc_value()))
print("BproX Price: {0}".format(moc_state.bprox_price()))
print("BproX Tec Price: {0}".format(moc_state.btc2x_tec_price()))
print("Days to settlement: {0}".format(moc_state.days_to_settlement()))
print("coverage: {0}".format(moc_state.coverage(bucket_x2)))
print("Is Liquidation: {0}".format(moc_state.is_liquidation()))

print("BproX rBTC: {0}".format(moc_state.bucket_nbtc(bucket_x2)))
print("BproX DOC: {0}".format(moc_state.bucket_ndoc(bucket_x2)))
print("BproX BTCX: {0}".format(moc_state.bucket_nbpro(bucket_x2)))



print("Is calculated: {0}".format(moc_state.is_calculate_ema()))
print("Price provider: {0}".format(moc_state.price_provider()))


moc_main = MoC(network_manager).from_abi()
print("Is Bucket Liquidation: {0}".format(moc_main.is_bucket_liquidation()))
print("is_settlement_enabled: {0}".format(moc_main.is_settlement_enabled()))
print("is_daily_enabled: {0}".format(moc_main.is_daily_enabled()))
print("is_bitpro_interest_enabled: {0}".format(moc_main.is_bitpro_interest_enabled()))
print("paused: {0}".format(moc_main.paused()))
#print("mint_bprox_gas_estimated: {0}".format(moc_main.mint_bprox_gas_estimated(0.001)))


# finally disconnect from network
network_manager.disconnect()

