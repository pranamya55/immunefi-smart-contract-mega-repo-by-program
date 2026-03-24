from moneyonchain.networks import network_manager
from moneyonchain.governance import BatchChanger
from moneyonchain.moc_vendors import VENDORSMoCInrate


import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/batch_changer_settlement.log',
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

targets_to_execute = list()
data_to_execute = list()

contract_moc_inrate = VENDORSMoCInrate(network_manager).from_abi()

targets_to_execute.append(contract_moc_inrate.address())
data_to_execute.append(contract_moc_inrate.sc.setBitProInterestBlockSpan.encode_input(40))

log.info("Targets to execute")
log.info(targets_to_execute)
log.info("Data to execute")
log.info(data_to_execute)

contract = BatchChanger(network_manager)

tx_receipt = contract.constructor(targets_to_execute, data_to_execute, execute_change=False)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
