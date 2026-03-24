"""
Get BPRO Price
Get Bitcoin Price
Get BTCX Price
"""

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoC

connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


contract = MoC(network_manager).from_abi()
print("Bitcoin price in usd: {0}".format(contract.bitcoin_price()))
print("BPRO price in usd: {0}".format(contract.bpro_price()))
print("BTC2X price in usd: {0}".format(contract.btc2x_tec_price() * contract.bitcoin_price()))

# finally disconnect from network
network_manager.disconnect()
