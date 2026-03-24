from moneyonchain.networks import network_manager
from moneyonchain.moc import MocInrateBitProInterestAddressChanger

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/changers_moc_inrate_bitpro_interest_address.log',
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


contract = MocInrateBitProInterestAddressChanger(network_manager)
bitpro_interest_address = '0xB64DC1c93573001551f32bC7443452e93A00344f'

if config_network in ['mocTestnetAlpha']:
    execute_change = True
else:
    execute_change = False

tx_receipt = contract.constructor(bitpro_interest_address, execute_change=execute_change)
if tx_receipt:
    print("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    print("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
