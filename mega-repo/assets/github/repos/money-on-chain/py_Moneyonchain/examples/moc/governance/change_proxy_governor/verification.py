import json
import os
from optparse import OptionParser

from moneyonchain.networks import network_manager
from moneyonchain.governance import Governed

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger('default')


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
                "python verification.py " \
                "--connection_network=rskTestnetPublic " \
                "--config_network=mocTestnetAlpha3 "

connection_network = options.connection_network
if not connection_network:
    raise Exception(usage_example)

config_network = options.config_network
if not connection_network:
    raise Exception(usage_example)


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

log.info('Connecting environment {0}...'.format(config_network))

proxy_addresses = settings[config_network]['proxyAddresses']

for proxy_address in proxy_addresses:
    address = settings[config_network]['proxyAddresses'][proxy_address]
    if not address:
        continue

    contract_governed = Governed(network_manager, contract_address=address).from_abi()

    log.info("Contract: {0}: {1} Governor: {2}".format(proxy_address, address, contract_governed.governor()))


# finally disconnect from network
network_manager.disconnect()
