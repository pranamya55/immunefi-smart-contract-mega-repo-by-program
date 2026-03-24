from moneyonchain.networks import network_manager
from moneyonchain.medianizer import PriceFeederAdderChanger


import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/changers_feedadder.log',
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


contract = PriceFeederAdderChanger(network_manager)

price_feeder_owner = '0x64dcc3bcbeae8ce586cabdef79104986beafcad6'
tx_receipt = contract.constructor(price_feeder_owner, execute_change=False)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")


# finally disconnect from network
network_manager.disconnect()
