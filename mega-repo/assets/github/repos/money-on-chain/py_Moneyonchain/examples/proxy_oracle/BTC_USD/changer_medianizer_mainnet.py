from moneyonchain.networks import network_manager
from moneyonchain.medianizer import ProxyMoCMedianizerChanger


import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/changer_medianizer.log',
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
config_network = 'proxyBTCUSDMainnet'

log.info("Connecting... Network: {0} Enviroment: {1}".format(connection_network, config_network))

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

proxy_oracle = '0x972a21C61B436354C0F35836195D7B67f54E482C'
new_medianizer = '0xe2927A0620b82A66D67F678FC9b826B0E01B1bFD'

contract = ProxyMoCMedianizerChanger(network_manager)

tx_receipt = contract.constructor(new_medianizer,
                                  contract_address_proxy_medianizer=proxy_oracle,
                                  execute_change=False)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
