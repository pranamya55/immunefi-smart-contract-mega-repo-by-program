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


connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


contract = MoCPriceProviderChanger(network_manager)
# BTC: 0xe2927A0620b82A66D67F678FC9b826B0E01B1bFD
price_provider = '0xe2927A0620b82A66D67F678FC9b826B0E01B1bFD'
tx_receipt = contract.constructor(price_provider, execute_change=False)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
