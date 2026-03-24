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


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


contract = MocInrateBitProInterestAddressChanger(network_manager)
bitpro_interest_address = '0xb908E56e1f386d6F955569a687d5286F7e49A90F'

if config_network in ['mocTestnetAlpha']:
    execute_change = True
else:
    execute_change = False

tx_receipt = contract.constructor(bitpro_interest_address, execute_change=execute_change)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
