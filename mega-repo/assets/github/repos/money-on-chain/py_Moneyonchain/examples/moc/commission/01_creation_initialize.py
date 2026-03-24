import json

from moneyonchain.networks import NetworkManager
from moneyonchain.moc import CommissionSplitter


import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/01_creation_initialize.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


def options_from_settings(filename='settings.json'):
    """ Options from file settings.json """

    with open(filename) as f:
        config_options = json.load(f)

    return config_options


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


# load settings from file
settings = options_from_settings()

splitter = CommissionSplitter(network_manager, contract_address=settings[config_network]['CommissionSplitter']).from_abi()

governor_address = network_manager.options['networks'][config_network]['addresses']['governor']
moc_address = network_manager.options['networks'][config_network]['addresses']['MoC']
comission_address = settings[config_network]['CommissionAddress']
moc_proportion = settings[config_network]['MocProportion']

log.info("Initializing contract with this parameters:")
log.info("Network: {0}".format(config_network))
log.info("MoC Address: {0}".format(moc_address))
log.info("Commission Address: {0}".format(comission_address))
log.info("Moc Proportion: {0}".format(moc_proportion))
log.info("Governor Address: {0}".format(governor_address))

tx_hash, tx_receipt = splitter.initialize(moc_address, comission_address, moc_proportion, governor_address)
if tx_receipt:
    log.info("Sucessfully initialized")
else:
    log.info("Error initialized")

# finally disconnect from network
network_manager.disconnect()
