import json

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoCSetCommissionMocProportionChanger


import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/changer_moc_inrate_proportion.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network = 'bscTestnetPrivate'
config_network = 'bnbTestnet'

# Connect to network
network_manager.connect(
    connection_network=connection_network,
    config_network=config_network)

contract_splitter = '0x3502F04d5b39945eA02d98251B0aB7267c0d605B'
contract = MoCSetCommissionMocProportionChanger(network_manager)

if config_network in ['bnbTestnet']:
    execute_change = True
else:
    execute_change = False

proportion = 200000000000000000
tx_receipt = contract.constructor(proportion,
                                  commission_splitter=contract_splitter,
                                  execute_change=execute_change)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
