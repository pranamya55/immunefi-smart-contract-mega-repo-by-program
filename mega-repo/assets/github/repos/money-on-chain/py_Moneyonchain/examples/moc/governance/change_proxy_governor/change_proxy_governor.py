"""

Proxy change IGovernor
To change the governor of proxy contract.

"""

import json
import os
from optparse import OptionParser

from moneyonchain.networks import network_manager
from moneyonchain.governance import ProxyAdminIGovernorChanger, Governed

import logging
import logging.config


usage = '%prog [options] '
parser = OptionParser(usage=usage)

parser.add_option('-n', '--connection_network', action='store', dest='connection_network', type="string",
                  help='network to connect')

parser.add_option('-e', '--config_network', action='store', dest='config_network', type="string",
                  help='enviroment to connect')

parser.add_option('-c', '--contract_name', action='store', dest='contract_name', type="string", help='contract name')

(options, args) = parser.parse_args()


def options_from_settings(filename='settings.json'):
    """ Options from file settings.json """

    with open(filename) as f:
        config_options = json.load(f)

    return config_options


def options_to_settings(json_content, filename='settings.json'):
    """ Options to file settings.json """

    with open(filename, 'w') as f:
        json.dump(json_content, f, indent=4)


# load settings from file
settings = options_from_settings()

usage_example = "Run example: " \
                "python change_governor.py " \
                "--connection_network=rskTestnetPublic " \
                "--config_network=mocTestnetAlpha3 " \
                "--contract_name=MoC"


connection_network = options.connection_network
if not connection_network:
    raise Exception(usage_example)

config_network = options.config_network
if not connection_network:
    raise Exception(usage_example)

contract_name = options.contract_name
if not contract_name:
    raise Exception(usage_example)

#connection_network = 'rskTestnetPublic'
#config_network = 'mocTestnetAlpha3'
#contract_name = 'MoC'
proxy_order = settings[config_network]['proxyOrder'][contract_name]

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/{0}_change_proxy_{1}.log'.format(proxy_order, contract_name),
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


log.info('Connecting enviroment {0}...'.format(config_network))
log.info('Change contract name: {0}_{1}...'.format(proxy_order, contract_name))

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


proxy_address = settings[config_network]['proxyAddresses'][contract_name]
log.info('Contract proxy address {0}...'.format(proxy_address))

contract_change_governor = Governed(network_manager, contract_address=proxy_address).from_abi()
log.info("Current Governor: {0}".format(contract_change_governor.governor()))

new_governor = settings[config_network]['targetGovernor']
execute_change = settings[config_network]['executeChange']

log.info("Target New Governor: {0}".format(new_governor))

contract_changer = ProxyAdminIGovernorChanger(network_manager)

tx_receipt = contract_changer.constructor(proxy_address,
                                          new_governor,
                                          execute_change=execute_change)
changer_address = ''
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
    changer_address = tx_receipt.contract_address
else:
    log.info("Error deploying changer")

settings[config_network]['changerAddresses']["{0}_{1}".format(proxy_order, contract_name)] = changer_address

options_to_settings(settings)

# finally disconnect from network
network_manager.disconnect()
