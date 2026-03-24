
from decimal import Decimal
from web3 import Web3
from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoC


import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()


connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnetAlpha'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


moc_sc = RDOCMoC(network_manager).from_abi()

print("Please wait to the transaction be mined!...")
tx_receipt = moc_sc.redeem_all_doc()

# finally disconnect from network
network_manager.disconnect()
