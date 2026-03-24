from moneyonchain.networks import network_manager
from moneyonchain.medianizer import RDOCPriceFeederAdderChanger

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/changers_feedadder_custom.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


contract = RDOCPriceFeederAdderChanger(network_manager)

price_feeder_owner = '0xA8f94D08D3D9C045fe0B86A953dF39B14206153c'
contract_address_medianizer = '0x01a165cC33Ff8Bd0457377379962232886be3DE6'
contract_address_feedfactory = '0xbB26D11bd2a9F2274cD1a8E571e5A352816acaEA'
tx_receipt = contract.constructor(price_feeder_owner,
                                   contract_address_medianizer=contract_address_medianizer,
                                   contract_address_feedfactory=contract_address_feedfactory,
                                   execute_change=False)
if tx_receipt:
    print("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    print("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
