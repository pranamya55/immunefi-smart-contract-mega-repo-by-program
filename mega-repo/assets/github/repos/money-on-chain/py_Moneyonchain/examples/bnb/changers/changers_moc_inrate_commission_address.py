import json
import logging
import logging.config

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoCInrateCommissionsAddressChanger


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/changers_moc_inrate_commission_address.log',
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
network_manager.connect(connection_network=connection_network, config_network=config_network)

contract = MoCInrateCommissionsAddressChanger(network_manager)

if config_network in ['bnbTestnet']:
    execute_change = True
else:
    execute_change = False

contract_splitter = '0x5F1984BdFB81EbA96E95693a08Aec4B5C853Da0C'
tx_receipt = contract.constructor(contract_splitter,
                                  execute_change=execute_change)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
