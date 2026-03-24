from moneyonchain.networks import network_manager
from moneyonchain.moc import MocInrateBtcxInterestChanger

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/changers_inrate_btcx_interest.log',
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

contract = MocInrateBtcxInterestChanger(network_manager)

btxc_tmin = int(0.00027378507871321 * 10 ** 18)
btxc_tmax = int(0.04 * 10 ** 18)
btxc_power = int(6)

tx_receipt = contract.constructor(btxc_tmin, btxc_tmax, btxc_power, execute_change=True)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
