from tabulate import tabulate
from web3 import Web3

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoC
from moneyonchain.moc_vendors import VENDORSMoC
from moneyonchain.governance import ProxyAdminInterface


connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

block_identifier = None
is_vendor = True

if is_vendor:
    moc_moc = VENDORSMoC(network_manager, load_sub_contract=False).from_abi().contracts_discovery()
else:
    moc_moc = MoC(network_manager, load_sub_contract=False).from_abi().contracts_discovery()

print("Connection to: {0}".format(config_network))
connector_addresses = moc_moc.connector_addresses()

if not block_identifier:
    block_identifier = network_manager.block_number

available_list = list()
available_list.append(('MoC', connector_addresses['MoC'], True))
available_list.append(('MoCConnector', moc_moc.connector(), True))
available_list.append(('MoCState', connector_addresses['MoCState'], True))
#available_list.append(('MoCConverter', connector_addresses['MoCConverter'], True))
available_list.append(('MoCSettlement', connector_addresses['MoCSettlement'], True))
available_list.append(('MoCExchange', connector_addresses['MoCExchange'], True))
available_list.append(('MoCInrate', connector_addresses['MoCInrate'], True))
#available_list.append(('MoCBurnout', connector_addresses['MoCBurnout'], True))
available_list.append(('DoCToken', connector_addresses['DoCToken'], False))
available_list.append(('BProToken', connector_addresses['BProToken'], False))
available_list.append(('MoCBProxManager', connector_addresses['MoCBProxManager'], True))
available_list.append(('MoCMedianizer', moc_moc.sc_moc_state.price_provider(), False))
available_list.append(('CommissionSplitter', moc_moc.sc_moc_inrate.commission_address(), True))
if is_vendor:
    available_list.append(('MoCOracle', moc_moc.sc_moc_state.moc_price_provider(), False))
    available_list.append(('MoCToken', moc_moc.sc_moc_state.moc_token(), False))
    available_list.append(('MoCVendors', moc_moc.sc_moc_state.moc_vendors(), True))


titles = ['Contract', 'Proxy', 'Implementation', 'Block Nº']
display_table = list()
for item in available_list:
    contract_implementation = ''
    if item[2]:
        contract_admin = ProxyAdminInterface(network_manager, contract_address=Web3.toChecksumAddress(item[1]))
        contract_implementation = contract_admin.implementation()
    display_table.append([item[0], item[1], contract_implementation, block_identifier])


print(tabulate(display_table, headers=titles, tablefmt="pipe"))
print()

# finally disconnect from network
network_manager.disconnect()
