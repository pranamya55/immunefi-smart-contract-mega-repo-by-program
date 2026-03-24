from moneyonchain.networks import network_manager
from moneyonchain.moc import MoCInrate, MoCState


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


moc_inrate = MoCInrate(network_manager).from_abi()
moc_state = MoCState(network_manager).from_abi()

print("BTCX Inrate")
print("===========")

# amount to mint
amount_value = 0.001

# get days to settlement from the contract
days_to_settlement = moc_state.days_to_settlement()

print("Interest of MINT {0} BTCX".format(amount_value))
interest_no_days = moc_inrate.btc2x_inrate_avg(amount_value, on_minting=True)

print("Current day to settlement: {0} Interest: {1}".format(days_to_settlement,
                                                            interest_no_days * days_to_settlement))
print("Current day to settlement: {0} Interest %: {1} %".format(days_to_settlement,
                                                                interest_no_days * days_to_settlement * 100))

print("Interest on minting...")
for day_to_sett in reversed(range(0, 30)):
    print("Days to settlement: {0} Interest: {1}".format(day_to_sett, interest_no_days * day_to_sett))

print("Interest on reedeeming...")
interest_no_days = moc_inrate.btc2x_inrate_avg(amount_value, on_minting=False)
for day_to_sett in reversed(range(0, 30)):
    print("Days to settlement: {0} Interest: {1}".format(day_to_sett, interest_no_days * day_to_sett))


# finally disconnect from network
network_manager.disconnect()
