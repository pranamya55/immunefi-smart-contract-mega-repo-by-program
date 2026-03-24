from moneyonchain.networks import network_manager
from moneyonchain.medianizer import RDOCPriceFeederRemoverChanger

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/changers_feedremover.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network = 'rskMainnetPublic'
config_network = 'rdocMainnet'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)


contract = RDOCPriceFeederRemoverChanger(network_manager)

contract_address_medianizer = '0x504EfCadFB020d6bBaeC8a5c5BB21453719d0E00'
contract_address_pricefeed = '0xBEd51D83CC4676660e3fc3819dfAD8238549B975'
tx_receipt = contract.constructor(contract_address_pricefeed,
                                  contract_address_medianizer=contract_address_medianizer,
                                  execute_change=False)
if tx_receipt:
    print("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    print("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
