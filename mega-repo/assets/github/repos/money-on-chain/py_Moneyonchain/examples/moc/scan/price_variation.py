from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoCState


connection_network = 'rskMainnetPublic'
config_network = 'rdocMainnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_state = RDOCMoCState(network_manager).from_abi()

bucket_x2 = moc_state.bucket_x2()
bucket_c0 = moc_state.bucket_c0()

old_block = network_manager.block_number - 2800
current_block = network_manager.block_number

print("Current block: {0}".format(current_block))
print("24hs ago block: {0}".format(old_block))

print("")
price_rif_1 = moc_state.bitcoin_price(block_identifier=old_block)
price_rif_2 = moc_state.bitcoin_price(block_identifier=current_block)
print("RIF Price   -24hs: {0}".format(price_rif_1))
print("RIF Price Current: {0}".format(price_rif_2))
print("Difference: {0}".format(price_rif_2-price_rif_1))

print("")
price_rifp_1 = moc_state.bpro_tec_price(block_identifier=old_block) * price_rif_1
price_rifp_2 = moc_state.bpro_tec_price(block_identifier=current_block) * price_rif_2
print("RIFP Price   -24hs: {0}".format(price_rifp_1))
print("RIFP Price Current: {0}".format(price_rifp_2))
print("Difference: {0}".format(price_rifp_2-price_rifp_1))

print("")
price_rifx_1 = moc_state.btc2x_tec_price(block_identifier=old_block) * price_rif_1
price_rifx_2 = moc_state.btc2x_tec_price(block_identifier=current_block) * price_rif_2
print("RIFX Price   -24hs: {0}".format(price_rifx_1))
print("RIFX Price Current: {0}".format(price_rifx_2))
print("Difference: {0}".format(price_rifx_2-price_rifx_1))


print("Technical prices")

print("")
price_rifp_1 = moc_state.bpro_tec_price(block_identifier=old_block)
price_rifp_2 = moc_state.bpro_tec_price(block_identifier=current_block)
print("RIFP Tec Price   -24hs: {0}".format(price_rifp_1))
print("RIFP Tec Price Current: {0}".format(price_rifp_2))
print("Difference: {0}".format(price_rifp_2-price_rifp_1))

print("")
price_rifx_1 = moc_state.btc2x_tec_price(block_identifier=old_block)
price_rifx_2 = moc_state.btc2x_tec_price(block_identifier=current_block)
print("RIFX TecPrice   -24hs: {0}".format(price_rifx_1))
print("RIFX Tec Price Current: {0}".format(price_rifx_2))
print("Difference: {0}".format(price_rifx_2-price_rifx_1))



# finally disconnect from network
network_manager.disconnect()
