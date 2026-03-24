"""
 brownie networks add BSCNetwork bscTestnet host=https://data-seed-prebsc-1-s1.binance.org:8545/ chainid=97 explorer=https://blockscout.com/rsk/mainnet/api
"""

from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoCState


connection_network = 'bscTestnet'
config_network = 'btcbAlphaTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_state = RDOCMoCState(network_manager).from_abi()

bucket_x2 = moc_state.bucket_x2()
print(bucket_x2)

bucket_c0 = moc_state.bucket_c0()
print(bucket_c0)


print("State: {0}".format(moc_state.state()))

print("Day Block Span: {0}".format(moc_state.day_block_span()))
print("Smoothing Factor: {0}".format(moc_state.smoothing_factor()))
print("RIF in system: {0}".format(moc_state.rbtc_in_system()))
print("Cobj: {0}".format(moc_state.cobj()))
print("Cobj X2: {0}".format(moc_state.cobj_X2()))
#print("Max mint riskpro avail: {0}".format(moc_state.max_mint_bpro_available()))
#print("Max mint riskpro: {0}".format(moc_state.max_mint_bpro()))
print("Absolute max doc: {0}".format(moc_state.absolute_max_doc()))
print("Max RISKPROx: {0}".format(moc_state.max_bprox(bucket_x2)))
#print("Max RISKPROx btc value: {0}".format(moc_state.max_bprox_btc_value()))
print("Absolute max bpro: {0}".format(moc_state.absolute_max_bpro()))
print("Free doc: {0}".format(moc_state.free_doc()))
print("Leverage: {0}".format(moc_state.leverage(bucket_x2)))


print("RIF Price in USD: {0}".format(moc_state.bitcoin_price()))
print("RIF Moving Average in USD: {0}".format(moc_state.bitcoin_moving_average()))
print("Days to settlement: {0}".format(moc_state.days_to_settlement()))
print("Global Coverage: {0}".format(moc_state.global_coverage()))
print("RIFP Total Supply: {0}".format(moc_state.bitpro_total_supply()))
print("RDOC Total Supply: {0}".format(moc_state.doc_total_supply()))
print("Implementation: {0}".format(moc_state.implementation()))

print("Max RISKPRO dicount {0}".format(moc_state.max_bpro_with_discount()))
print("RiskPro discount price {0}".format(moc_state.bpro_discount_price()))
print("RIFP Discount: {0}".format(moc_state.bpro_discount_rate()))
print("RiskPro price {0}".format(moc_state.bpro_price()))
print("RIFP Tec Price: {0}".format(moc_state.bpro_tec_price()))

print("RISKPROX Price: {0}".format(moc_state.bprox_price()))
print("RISKPROX Tec Price: {0}".format(moc_state.btc2x_tec_price()))

print("Inrate bag: {0}".format(moc_state.get_inrate_bag(bucket_x2)))


print("X2")
print("Bucket NBTC: {0}".format(moc_state.bucket_nbtc(bucket_x2)))
print("Bucket NDOC: {0}".format(moc_state.bucket_ndoc(bucket_x2)))
print("Bucket NBPRO: {0}".format(moc_state.bucket_nbpro(bucket_x2)))
print("Coverage RISKPROX: {0}".format(moc_state.coverage(bucket_x2)))

print("C0")
print("Bucket NBTC: {0}".format(moc_state.bucket_nbtc(bucket_c0)))
print("Bucket NDOC: {0}".format(moc_state.bucket_ndoc(bucket_c0)))
print("Bucket NBPRO: {0}".format(moc_state.bucket_nbpro(bucket_c0)))
print("Coverage RISKPRO: {0}".format(moc_state.coverage(bucket_c0)))


print("Is liquidation: {0}".format(moc_state.is_liquidation()))
print("Is calculate ema: {0}".format(moc_state.is_calculate_ema()))
print("Price provider: {0}".format(moc_state.price_provider()))

print("Liquidation price: {0}".format(moc_state.liquidation_price()))

print("Global locked reserve: {0}".format(moc_state.global_locked_reserve_tokens()))
print("Reserves remainder: {0}".format(moc_state.reserves_remainder()))
print("Liq: {0}".format(moc_state.liq()))

#print("Current_abundance_ratio: {0}".format(moc_state.current_abundance_ratio()))  #block_identifier=1233780
#print("abundance_ratio: {0}".format(moc_state.abundance_ratio(int(2.242807702008664948*10*18)))) #, block_identifier=1233780


print("Bucket NDOC: {0}".format(moc_state.bucket_ndoc(bucket_c0, formatted=False)))
print("RDOC Totaly: {0}".format(moc_state.doc_total_supply(formatted=False)))
print("Bucket NBTC: {0}".format(moc_state.bucket_nbtc(bucket_c0, formatted=False)))
print("RIF in sysm: {0}".format(moc_state.rbtc_in_system(formatted=False)))


print()
print("Vendors STATS:")
print("==============")
print("MoC Price: {0}".format(moc_state.moc_price()))
print("MoC Price Provider: {0}".format(moc_state.moc_price_provider()))
print("MoC Token: {0}".format(moc_state.moc_token()))
print("MoC Vendors: {0}".format(moc_state.moc_vendors()))
print("Protected: {0}".format(moc_state.protected()))
print("Liquidation enabled: {0}".format(moc_state.liquidation_enabled()))



# finally disconnect from network
network_manager.disconnect()
