from moneyonchain.networks import network_manager
from moneyonchain.moc import MoCState


connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)

# Getting MoCState Contract
moc_state = MoCState(network_manager).from_abi()

# get bitcoin price from contract
B = moc_state.bitcoin_price()

# get Moving average Price
EMA = moc_state.bitcoin_moving_average()

# consevative price
Bcons = min(B, EMA)

# cob objective
cob = moc_state.cobj()

# calculate cob objective conservative adjust
Cobj = float(cob * (B / Bcons))

print("B: {0}".format(B))
print("EMA: {0}".format(EMA))
print("Bcons: {0}".format(Bcons))
print("cob: {0}".format(cob))
print("Cobj real: {0}".format(Cobj))

# finally disconnect from network
network_manager.disconnect()
