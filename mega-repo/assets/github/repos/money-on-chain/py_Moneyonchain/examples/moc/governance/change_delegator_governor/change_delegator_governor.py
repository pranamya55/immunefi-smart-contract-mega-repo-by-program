"""

Change Upgrade delegator Governor

"""

import json
from optparse import OptionParser

from moneyonchain.networks import network_manager
from moneyonchain.governance import UpgradeDelegatorIGovernorChanger

import logging
import logging.config


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/change_delegator_governor.log',
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
                "python change_delegator_governor.py " \
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

new_governor = settings[config_network]['targetGovernor']
execute_change = settings[config_network]['executeChange']

upgrade_delegator = network_manager.options['networks'][config_network]['addresses']['upgradeDelegator']

log.info("Current upgrade delegator: {0}".format(upgrade_delegator))
log.info("Target New Governor: {0}".format(new_governor))

contract_changer = UpgradeDelegatorIGovernorChanger(network_manager)

tx_receipt = contract_changer.constructor(upgrade_delegator,
                                          new_governor,
                                          execute_change=execute_change)

if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
