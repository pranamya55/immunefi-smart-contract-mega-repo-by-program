from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCCommissionSplitter
from moneyonchain.tokens import RIF

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()

connection_network = 'rskMainnetPublic'
config_network = 'rdocMainnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


splitter = RDOCCommissionSplitter(network_manager, contract_address='0x4C42DBa2a88D4ecc97aA7F28Ced17b4e60523201').from_abi()

token_rif = RIF(network_manager).from_abi()

print("Contract address:")
print(splitter.commission_address())

print("MoC Address")
print(splitter.moc_address())

print("Reserve Address")
print(splitter.reserve_address())

print("Proportion:")
print(splitter.moc_proportion())

print("Balance RBTC:")
print(splitter.balance())

print("Balance RIF:")
print(token_rif.balance_of(splitter.address()))

# finally disconnect from network
network_manager.disconnect()
