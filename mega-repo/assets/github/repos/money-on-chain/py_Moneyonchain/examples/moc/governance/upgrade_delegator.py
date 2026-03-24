from moneyonchain.networks import network_manager
from moneyonchain.governance import UpgradeDelegator, ProxyAdmin

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger('default')

# Connect to network
network_manager.connect(connection_network='rskTestnetPublic', config_network='mocTestnetAlpha')


upgrade_delegator = UpgradeDelegator(network_manager).from_abi()
proxy_admin_address = upgrade_delegator.get_proxy_admin('0x01AD6f8E884ed4DDC089fA3efC075E9ba45C9039')

contract_admin = ProxyAdmin(network_manager).from_abi()

log.info("Owner: {0}".format(contract_admin.owner()))
log.info("Upgrade delegator: {0}".format(upgrade_delegator.address()))
log.info("Upgrade delegator: -> Proxy Admin {0}".format(upgrade_delegator.proxy_admin()))
log.info("Proxy Admin: {0}".format(contract_admin.address()))
log.info("Admin: {0}".format(proxy_admin_address))
log.info("Governor: {0}".format(upgrade_delegator.governor()))

# finally disconnect from network
network_manager.disconnect()
