from moneyonchain.networks import network_manager
from moneyonchain.medianizer import PriceFeederWhitelistChanger

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

connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


contract = PriceFeederWhitelistChanger(network_manager)

contract_address_medianizer = '0x7B19bb8e6c5188eC483b784d6fB5d807a77b21bF'
contract_address_pricefeed = '0xE94007E81412eDfdB87680F768e331E8c691f0e1'
tx_receipt = contract.constructor(contract_address_pricefeed,
                                  contract_address_medianizer=contract_address_medianizer,
                                  execute_change=False)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()

