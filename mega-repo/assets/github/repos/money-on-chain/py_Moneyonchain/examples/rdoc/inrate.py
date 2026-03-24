from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoCInrate, RDOCMoC

import logging
import logging.config

# logging module
# Initialize you log configuration using the base class
logging.basicConfig(level=logging.INFO)
# Retrieve the logger instance
log = logging.getLogger()

connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


moc_inrate = RDOCMoCInrate(network_manager).from_abi()

print("Bitpro rate: {0}".format(moc_inrate.bitpro_rate()))

print("RDOC Freestable reedeem")
print("=======================")
info = moc_inrate.stable_inrate()
print(info)

print("Interest of reedeeming 1000 DOC")
interest_no_days = moc_inrate.doc_inrate_avg(1)

for day_to_sett in reversed(range(0, 30)):
    print("Days to settlement: {0} Interest: {1}".format(day_to_sett, interest_no_days * day_to_sett))

print("RIFX Inrate")
print("===========")
info = moc_inrate.riskprox_inrate()
print(info)

print("Interest of MINT 1.0 RIFX")
interest_no_days = moc_inrate.btc2x_inrate_avg(0.00000001, on_minting=True)

for day_to_sett in reversed(range(0, 30)):
    print("Days to settlement: {0} Interest: {1}".format(day_to_sett, interest_no_days * day_to_sett))

print("Interest of REEDEEM 1.0 RIFX")
interest_no_days = moc_inrate.btc2x_inrate_avg(2.0, on_minting=False)

for day_to_sett in reversed(range(0, 30)):
    print("Days to settlement: {0} Interest: {1}".format(day_to_sett, interest_no_days * day_to_sett))

info = moc_inrate.calc_mint_interest_value(1.0)
print(info)

# finally disconnect from network
network_manager.disconnect()
