from decimal import Decimal
import time
import datetime
import math
from web3 import Web3

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoCInrate


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


print("Connecting to MoCInrate")
moc_inrate = MoCInrate(network_manager).from_abi()

amount = Decimal(0.00001)

count = 0
print("Variation interest in every 30seconds")
while count <= 300:
    mint_interest = moc_inrate.calc_mint_interest_value(amount)
    print("Count: {0}s interest: {1:.18f} timestamp: {2}".format(count,
                                                                 mint_interest,
                                                                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    count += 30
    time.sleep(30)

# finally disconnect from network
network_manager.disconnect()
