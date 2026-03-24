import json
import os
from optparse import OptionParser

from moneyonchain.networks import network_manager
from moneyonchain.governance import Governed, UpgradeDelegator, ProxyAdmin

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

log.info('Connecting enviroment {0}...'.format(config_network))

proxy_addresses = settings[config_network]['proxyAddresses']

upgrade_delegator = UpgradeDelegator(network_manager).from_abi()
contract_admin = ProxyAdmin(network_manager).from_abi()
log.info("Upgrade delegator: {0}".format(upgrade_delegator.address()))
log.info("Upgrade delegator Governor: {0}".format(upgrade_delegator.governor()))
log.info("Proxy Admin: {0}".format(contract_admin.address()))
log.info("")

for proxy_address in proxy_addresses:
    address = settings[config_network]['proxyAddresses'][proxy_address]
    if not address:
        continue

    log.info("Contract: {0}: {1} ".format(proxy_address, address))
    error = False
    try:
        proxy_admin_address = upgrade_delegator.get_proxy_admin(address)
    except:
        proxy_admin_address = None
        log.info("Error! Proxy admin is not controlled by current upgrade delegator")

    if proxy_admin_address and proxy_admin_address == upgrade_delegator.proxy_admin():
        log.info("OK: Proxy admin are equal {0} / {1}".format(proxy_admin_address, upgrade_delegator.proxy_admin()))
    else:
        log.info("Error: Proxy admin are not equal {0} / {1} (Except on Upgrade Delegator)".format(
            proxy_admin_address, upgrade_delegator.proxy_admin()))

    if contract_admin.owner() == upgrade_delegator.address():
        log.info("OK: Contract admin owner is upgrade delegator {0} / {1}".format(
            contract_admin.owner(), upgrade_delegator.address()))
    else:
        log.info("Error: Contract admin owner is not upgrade delegator {0} / {1}".format(
            contract_admin.owner(), upgrade_delegator.address()))

    log.info("")


# finally disconnect from network
network_manager.disconnect()
