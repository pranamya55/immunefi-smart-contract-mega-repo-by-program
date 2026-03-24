import json
import logging
import logging.config

from moneyonchain.networks import NetworkManager
from moneyonchain.moc import MoCSetCommissionFinalAddressChanger


def options_from_settings(filename='settings.json'):
    """ Options from file settings.json """

    with open(filename) as f:
        config_options = json.load(f)

    return config_options


import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/11_changer_commission.log',
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

# init network manager
# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager = NetworkManager(
    connection_network=connection_network,
    config_network=config_network)

# run install() if is the first time and you want to install
# networks connection from brownie
# network_manager.install()

# Connect to network
network_manager.connect()


# load settings from file, take a look on settings.json
settings = options_from_settings()

contract_splitter = settings[config_network]['CommissionSplitter']
contract = MoCSetCommissionFinalAddressChanger(network_manager)

if config_network in ['mocTestnetAlpha']:
    execute_change = True
else:
    execute_change = False

beneficiary_address = '0xf69287F5Ca3cC3C6d3981f2412109110cB8af076'
tx_receipt = contract.constructor(beneficiary_address,
                                  commission_splitter=contract_splitter,
                                  execute_change=execute_change)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
