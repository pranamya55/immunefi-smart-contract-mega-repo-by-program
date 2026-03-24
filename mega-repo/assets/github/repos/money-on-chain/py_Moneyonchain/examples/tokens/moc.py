from moneyonchain.networks import network_manager
from moneyonchain.tokens import MoCToken

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()

connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


token = MoCToken(network_manager, contract_address='0x9AC7fE28967B30E3A4e6e03286d715b42B453D10').from_abi()

print(token.name())
print(token.symbol())
print(token.total_supply())
print(token.owner())

# # this is our account we want to allow
# account = '0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3'
#
# # our dex address
# dex_address = '0xA066d6e20e122deB1139FA3Ae3e96d04578c67B5'
#
# # amount to allow
# amount_allow = 0.0001
#
# print(bit.allowance(account, dex_address))
#
# # if you want to set allowance
# #tx_receipt = bit.approve(dex_address, amount_allow)
# #print(tx_receipt)

# finally disconnect from network
network_manager.disconnect()
