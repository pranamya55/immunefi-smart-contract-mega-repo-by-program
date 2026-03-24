from moneyonchain.networks import network_manager
from moneyonchain.medianizer import RDOCPriceFeederWhitelistChanger

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/changers_feedwhitelist.log',
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
config_network = 'rdocTestnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


contract = RDOCPriceFeederWhitelistChanger(network_manager)

contract_address_medianizer = '0x9d4b2c05818A0086e641437fcb64ab6098c7BbEc'
contract_address_pricefeed = '0xE0A3dce741b7EaD940204820B78E7990a136EAC1'
tx_receipt = contract.constructor(contract_address_pricefeed,
                                  contract_address_medianizer=contract_address_medianizer,
                                  execute_change=False)
if tx_receipt:
    print("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    print("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()

