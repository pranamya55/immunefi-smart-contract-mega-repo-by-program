from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMocInrateRiskProInterestAddressChanger

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/changers_moc_inrate_riskpro_interest_address.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network = 'rskMainnetPublic'
config_network = 'rdocMainnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


contract = RDOCMocInrateRiskProInterestAddressChanger(network_manager)

riskpro_interest_address = '0x728967DD751F5f21bF390eeE66527dBC17bD7E25'

tx_receipt = contract.constructor(riskpro_interest_address, execute_change=False)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
