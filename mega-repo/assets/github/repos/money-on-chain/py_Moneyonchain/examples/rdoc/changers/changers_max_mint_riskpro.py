from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoCStateMaxMintRiskProChanger


import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/changers_max_mint_riskpro.log',
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

log.info('Connecting enviroment {0}...'.format(config_network))

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

contract = RDOCMoCStateMaxMintRiskProChanger(network_manager)

max_mint_riskpro = int(1000000000 * 10 ** 18)
tx_receipt = contract.constructor(max_mint_riskpro, execute_change=False)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
