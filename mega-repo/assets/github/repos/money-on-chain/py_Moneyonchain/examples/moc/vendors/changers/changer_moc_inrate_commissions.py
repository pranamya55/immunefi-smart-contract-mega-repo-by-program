from moneyonchain.networks import network_manager
from moneyonchain.moc_vendors import VENDORSMoCInrate, MoCInrateCommissionsChanger

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/changers_moc_inrate_commissions.log',
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

commission_rates = {
    "mint_bpro_fees_rbtc": int(0.001 * 10 ** 18),
    "redeem_bpro_fees_rbtc": int(0.001 * 10 ** 18),
    "mint_doc_fees_rbtc": int(0.001 * 10 ** 18),
    "redeem_doc_fees_rbtc": int(0.001 * 10 ** 18),
    "mint_btcx_fees_rbtc": int(0.001 * 10 ** 18),
    "redeem_btcx_fees_rbtc": int(0.001 * 10 ** 18),
    "mint_bpro_fees_moc": int(0.0005 * 10 ** 18),
    "redeem_bpro_fees_moc": int(0.0005 * 10 ** 18),
    "mint_doc_fees_moc": int(0.0005 * 10 ** 18),
    "redeem_doc_fees_moc": int(0.0005 * 10 ** 18),
    "mint_btcx_fees_moc": int(0.0005 * 10 ** 18),
    "redeem_btcx_fees_moc": int(0.0005 * 10 ** 18),
}

moc_inrate = VENDORSMoCInrate(network_manager).from_abi()
sc_rates = list()

rate = commission_rates['mint_bpro_fees_rbtc']
tx_type = moc_inrate.tx_type_mint_bpro_fees_rbtc()
sc_rates.append((tx_type, rate))

rate = commission_rates['redeem_bpro_fees_rbtc']
tx_type = moc_inrate.tx_type_redeem_bpro_fees_rbtc()
sc_rates.append((tx_type, rate))

rate = commission_rates['mint_doc_fees_rbtc']
tx_type = moc_inrate.tx_type_mint_doc_fees_rbtc()
sc_rates.append((tx_type, rate))

rate = commission_rates['redeem_doc_fees_rbtc']
tx_type = moc_inrate.tx_type_redeem_doc_fees_rbtc()
sc_rates.append((tx_type, rate))

rate = commission_rates['mint_btcx_fees_rbtc']
tx_type = moc_inrate.tx_type_mint_btcx_fees_rbtc()
sc_rates.append((tx_type, rate))

rate = commission_rates['redeem_btcx_fees_rbtc']
tx_type = moc_inrate.tx_type_redeem_btcx_fees_rbtc()
sc_rates.append((tx_type, rate))

rate = commission_rates['mint_bpro_fees_moc']
tx_type = moc_inrate.tx_type_mint_bpro_fees_moc()
sc_rates.append((tx_type, rate))

rate = commission_rates['redeem_bpro_fees_moc']
tx_type = moc_inrate.tx_type_redeem_bpro_fees_moc()
sc_rates.append((tx_type, rate))

rate = commission_rates['mint_doc_fees_moc']
tx_type = moc_inrate.tx_type_mint_doc_fees_moc()
sc_rates.append((tx_type, rate))

rate = commission_rates['redeem_doc_fees_moc']
tx_type = moc_inrate.tx_type_redeem_doc_fees_moc()
sc_rates.append((tx_type, rate))

rate = commission_rates['mint_btcx_fees_moc']
tx_type = moc_inrate.tx_type_mint_btcx_fees_moc()
sc_rates.append((tx_type, rate))

rate = commission_rates['redeem_btcx_fees_moc']
tx_type = moc_inrate.tx_type_redeem_btcx_fees_moc()
sc_rates.append((tx_type, rate))

contract = MoCInrateCommissionsChanger(network_manager)

print(sc_rates)

tx_receipt = contract.constructor(sc_rates, execute_change=True)
if tx_receipt:
    print("Changer Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    print("Error deploying changer")

# finally disconnect from network
network_manager.disconnect()
