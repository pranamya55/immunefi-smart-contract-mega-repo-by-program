import json
from optparse import OptionParser

from moneyonchain.networks import network_manager
from moneyonchain.governance import BatchChanger, UpgradeDelegator


import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/batch_changer_implementations.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


usage = '%prog [options] '
parser = OptionParser(usage=usage)

parser.add_option('-n', '--connection_network', action='store', dest='connection_network', type="string",
                  help='network to connect')

parser.add_option('-e', '--config_network', action='store', dest='config_network', type="string",
                  help='enviroment to connect')


(options, args) = parser.parse_args()


def options_from_settings(filename='settings.json'):
    """ Options from file settings.json """

    with open(filename) as f:
        config_options = json.load(f)

    return config_options


# load settings from file
settings = options_from_settings()

usage_example = "Run example: " \
                "python batch_changer_implementations.py " \
                "--connection_network=rskTestnetPublic " \
                "--config_network=mocTestnetAlpha3 "


connection_network = options.connection_network
if not connection_network:
    raise Exception(usage_example)

config_network = options.config_network
if not connection_network:
    raise Exception(usage_example)


log.info('Connecting enviroment {0}...'.format(config_network))

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

execute_change = settings[config_network]['executeChange']

targets_to_execute = list()
data_to_execute = list()

upgrade_delegator = UpgradeDelegator(network_manager).from_abi()


# CommissionSplitter
proxy_address = settings[config_network]['proxies']['MoCSettlement']
implementation_address = settings[config_network]['implementations']['MoCSettlement']

targets_to_execute.append(upgrade_delegator.address())
data_to_execute.append(upgrade_delegator.sc.upgrade.encode_input(proxy_address, implementation_address))


log.info("Targets to execute")
log.info(targets_to_execute)
log.info("Data to execute")
log.info(data_to_execute)

contract = BatchChanger(network_manager)

tx_receipt = contract.constructor(targets_to_execute, data_to_execute, execute_change=execute_change)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
