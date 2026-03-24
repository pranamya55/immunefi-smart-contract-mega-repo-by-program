from moneyonchain.networks import network_manager
from moneyonchain.moc import MoC


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

print("Connecting to MoC Contract ...")
moc_contract = MoC(network_manager).from_abi()
moc_address = moc_contract.address()

if moc_contract.mode != 'MoC':
    raise Exception("Note: This script is only for MOC mode contract ...")

print("RBTC Balance of contract: {0} balance: {1}".format(
    moc_address,
    moc_contract.rbtc_balance_of(moc_address)))

# finally disconnect from network
network_manager.disconnect()