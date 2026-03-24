from moneyonchain.networks import network_manager
from moneyonchain.governance import BatchChanger
from moneyonchain.moc import MoCInrate


import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/batch_changer_commission_rate.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network = 'bscTestnetPrivate'
config_network = 'bnbTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

MINT_BPRO_FEES_RBTC = '1'
REDEEM_BPRO_FEES_RBTC = '2'
MINT_DOC_FEES_RBTC = '3'
REDEEM_DOC_FEES_RBTC = '4'
MINT_BTCX_FEES_RBTC = '5'
REDEEM_BTCX_FEES_RBTC = '6'
MINT_BPRO_FEES_MOC = '7'
REDEEM_BPRO_FEES_MOC = '8'
MINT_DOC_FEES_MOC = '9'
REDEEM_DOC_FEES_MOC = '10'
MINT_BTCX_FEES_MOC = '11'
REDEEM_BTCX_FEES_MOC = '12'

FEES_RBTC = 0.001 * 10 ** 18
FEES_MOC = 0.0005 * 10 ** 18


targets_to_execute = list()
data_to_execute = list()

contract_moc_inrate = MoCInrate(network_manager).from_abi()

targets_to_execute.append(contract_moc_inrate.address())
data_to_execute.append(contract_moc_inrate.sc.setCommissionRateByTxType.encode_input(MINT_BPRO_FEES_RBTC, FEES_RBTC))

targets_to_execute.append(contract_moc_inrate.address())
data_to_execute.append(contract_moc_inrate.sc.setCommissionRateByTxType.encode_input(REDEEM_BPRO_FEES_RBTC, FEES_RBTC))

targets_to_execute.append(contract_moc_inrate.address())
data_to_execute.append(contract_moc_inrate.sc.setCommissionRateByTxType.encode_input(MINT_DOC_FEES_RBTC, FEES_RBTC))

targets_to_execute.append(contract_moc_inrate.address())
data_to_execute.append(contract_moc_inrate.sc.setCommissionRateByTxType.encode_input(REDEEM_DOC_FEES_RBTC, FEES_RBTC))

targets_to_execute.append(contract_moc_inrate.address())
data_to_execute.append(contract_moc_inrate.sc.setCommissionRateByTxType.encode_input(MINT_BTCX_FEES_RBTC, FEES_RBTC))

targets_to_execute.append(contract_moc_inrate.address())
data_to_execute.append(contract_moc_inrate.sc.setCommissionRateByTxType.encode_input(REDEEM_BTCX_FEES_RBTC, FEES_RBTC))

targets_to_execute.append(contract_moc_inrate.address())
data_to_execute.append(contract_moc_inrate.sc.setCommissionRateByTxType.encode_input(MINT_BPRO_FEES_MOC, FEES_MOC))

targets_to_execute.append(contract_moc_inrate.address())
data_to_execute.append(contract_moc_inrate.sc.setCommissionRateByTxType.encode_input(REDEEM_BPRO_FEES_MOC, FEES_MOC))

targets_to_execute.append(contract_moc_inrate.address())
data_to_execute.append(contract_moc_inrate.sc.setCommissionRateByTxType.encode_input(MINT_DOC_FEES_MOC, FEES_MOC))

targets_to_execute.append(contract_moc_inrate.address())
data_to_execute.append(contract_moc_inrate.sc.setCommissionRateByTxType.encode_input(REDEEM_DOC_FEES_MOC, FEES_MOC))

targets_to_execute.append(contract_moc_inrate.address())
data_to_execute.append(contract_moc_inrate.sc.setCommissionRateByTxType.encode_input(MINT_BTCX_FEES_MOC, FEES_MOC))

targets_to_execute.append(contract_moc_inrate.address())
data_to_execute.append(contract_moc_inrate.sc.setCommissionRateByTxType.encode_input(REDEEM_BTCX_FEES_MOC, FEES_MOC))

log.info("Targets to execute")
log.info(targets_to_execute)
log.info("Data to execute")
log.info(data_to_execute)

contract = BatchChanger(network_manager)

tx_receipt = contract.constructor(targets_to_execute, data_to_execute, execute_change=True)
if tx_receipt:
    log.info("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
