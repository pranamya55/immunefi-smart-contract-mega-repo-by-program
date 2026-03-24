from moneyonchain.networks import network_manager
from moneyonchain.medianizer import PriceFeederRemoverChanger


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
config_network = 'mocMainnet2'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


contract = PriceFeederRemoverChanger(network_manager)

contract_address_medianizer = '0x78c892Dc5b7139d0Ec1eF513C9E28eDfAA44f2d4'
contract_address_pricefeed = '0x5d111d1b49Aa39d0172712266B0DE2F1eB9957F4'
tx_receipt = contract.constructor(contract_address_pricefeed,
                                  contract_address_medianizer=contract_address_medianizer,
                                  execute_change=False)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()

