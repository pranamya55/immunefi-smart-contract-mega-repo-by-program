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


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


contract = MoCPriceProviderChanger(network_manager)
# BTC: 0x667bd3d048FaEBb85bAa0E9f9D87cF4c8CDFE849
# RIF: 0x9315AFD6aEc0bb1C1FB3fdcdC2E43797B0A61853
#price_provider = '0x2d39Cc54dc44FF27aD23A91a9B5fd750dae4B218'
#price_provider = '0x26a00aF444928d689DDEC7b4D17c0E4a8c9D407d'
#price_provider = '0x78c892Dc5b7139d0Ec1eF513C9E28eDfAA44f2d4'
price_provider = '0xbffBD993FF1d229B0FfE55668F2009d20d4F7C5f'
#price_provider = '0x4A4D3130905Ec11C648D10EA494a0F0FD95a13Ad'  # <--- No usar mockup
tx_receipt = contract.constructor(price_provider, execute_change=False)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
