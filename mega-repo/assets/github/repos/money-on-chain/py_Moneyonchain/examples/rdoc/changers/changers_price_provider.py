from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCPriceProviderChanger

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

connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnetAlpha'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

contract = RDOCPriceProviderChanger(network_manager)

#price_provider = '0x2B54819531B7126bDEE2CeFDD9c5342d6c307595'
#price_provider = '0x01a165cC33Ff8Bd0457377379962232886be3DE6'
#price_provider = '0x9d4b2c05818A0086e641437fcb64ab6098c7BbEc'
#price_provider = '0x9315AFD6aEc0bb1C1FB3fdcdC2E43797B0A61853'
##price_provider = '0xb856Ca7c722cfb202D81c55DC7925e02ed3f0A2F'
#price_provider = '0x987ccC60c378a61d167B6DD1EEF7613c6f63938f'
#price_provider = '0xDC3551f16FfDeBAa3Cb8D3b6C16d2A5bB9646dA4'
price_provider = '0x9d4b2c05818A0086e641437fcb64ab6098c7BbEc'
#price_provider = '0xb8deE36b3488E205aB8E5Fd2502e4104917F46FF'
tx_receipt = contract.constructor(price_provider, execute_change=False)
if tx_receipt:
    print("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    print("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
