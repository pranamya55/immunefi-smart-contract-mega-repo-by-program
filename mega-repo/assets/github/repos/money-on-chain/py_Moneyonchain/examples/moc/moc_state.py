from moneyonchain.networks import NetworkManager
from moneyonchain.moc import MoCState


connection_network='rskMainnetPublic'
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
print("Bitcoin Price in USD: {0}".format(moc_state.bitcoin_price()))
print("Bitcoin Moving Average in USD: {0}".format(moc_state.bitcoin_moving_average()))
print("Days to settlement: {0}".format(moc_state.days_to_settlement()))
print("Global Coverage: {0}".format(moc_state.global_coverage()))
print("Bitpro Total Supply: {0}".format(moc_state.bitpro_total_supply()))
print("DOC Total Supply: {0}".format(moc_state.doc_total_supply()))
print("Implementation: {0}".format(moc_state.implementation()))
print("BPro Discount: {0}".format(moc_state.bpro_discount_rate()))
print("BPro Tec Price: {0}".format(moc_state.bpro_tec_price()))
print("Cobj: {0}".format(moc_state.cobj()))
print("Smothing factor: {0}".format(moc_state.smoothing_factor()))
# finally disconnect from network
network_manager.disconnect()
