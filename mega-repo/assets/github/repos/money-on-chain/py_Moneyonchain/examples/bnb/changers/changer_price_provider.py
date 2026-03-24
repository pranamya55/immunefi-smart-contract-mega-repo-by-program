from moneyonchain.networks import network_manager
from moneyonchain.moc import MoCPriceProviderChanger

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/changers_price_provider.log',
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
config_network = 'bnbAlphaTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

contract = MoCPriceProviderChanger(network_manager)
price_provider = '0x6cf318ecf1Cd101755ccdA027B1D47B48b542cBA'
tx_receipt = contract.constructor(price_provider, execute_change=True)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
