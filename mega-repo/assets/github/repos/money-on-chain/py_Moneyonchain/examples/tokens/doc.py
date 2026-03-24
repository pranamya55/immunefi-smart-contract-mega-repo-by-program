from moneyonchain.networks import NetworkManager
from moneyonchain.tokens.doc import DoCToken

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()

# init network manager
# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager = NetworkManager(
    connection_network='rskTestnetPublic',
    config_network='mocTestnet')

# run install() if is the first time and you want to install
# networks connection from brownie
# network_manager.install()

# Connect to network
network_manager.connect()

# Instantiate BitPro Token Contract from abi
bit = DoCToken(network_manager).from_abi()

print(bit.name())
print(bit.symbol())
print(bit.total_supply())

# this is our account we want to allow
account = '0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3'

# our dex address
dex_address = '0xA066d6e20e122deB1139FA3Ae3e96d04578c67B5'

# amount to allow
amount_allow = 0.0001

print(bit.allowance(account, dex_address))

# if you want to set allowance
#tx_receipt = bit.approve(dex_address, amount_allow)
#print(tx_receipt)

# finally disconnect from network
network_manager.disconnect()
