import json
from optparse import OptionParser

from moneyonchain.networks import network_manager
from moneyonchain.governance import SkipVotingProcessChange


import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/skip_voting_process.log',
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
                "python skip_voting_process.py " \
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

contract = SkipVotingProcessChange(network_manager)

voting_machine_address = settings[config_network]['skipVoting']['voting_machine_address']
governor_address = settings[config_network]['skipVoting']['governor_address']
changer_address = settings[config_network]['skipVoting']['changer_address']
execute_change = settings[config_network]['executeChange']

log.info('Voting machine address {0}...'.format(voting_machine_address))
log.info('Governor address {0}...'.format(governor_address))
log.info('Changer address {0}...'.format(changer_address))
log.info('Execute Change {0}...'.format(execute_change))

tx_receipt = contract.constructor(
    voting_machine_address,
    governor_address,
    changer_address,
    execute_change=execute_change)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
