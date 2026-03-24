"""

Event proxy admin

"""

import time
from web3 import Web3

from moneyonchain.networks import network_manager
from moneyonchain.governance import EventUpgradeabilityProxyUpgraded
from moneyonchain.moc import MoC
from moneyonchain.moc_vendors import VENDORSMoC
from moneyonchain.governance import ProxyAdminInterface

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/event_proxy_admin.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network = 'rskTestnetLocal'
config_network = 'mocTestnetAlpha'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

log.info("Starting to import events from contract...")
start_time = time.time()

print("Connection to: {0}".format(config_network))

is_vendor = True

if is_vendor:
    moc_moc = VENDORSMoC(network_manager, load_sub_contract=False).from_abi().contracts_discovery()
else:
    moc_moc = MoC(network_manager, load_sub_contract=False).from_abi().contracts_discovery()

connector_addresses = moc_moc.connector_addresses()

available_list = list()
available_list.append(('MoC', connector_addresses['MoC'], True))
available_list.append(('MoCConnector', moc_moc.connector(), True))
available_list.append(('MoCState', connector_addresses['MoCState'], True))
available_list.append(('MoCConverter', connector_addresses['MoCConverter'], True))
available_list.append(('MoCSettlement', connector_addresses['MoCSettlement'], True))
available_list.append(('MoCExchange', connector_addresses['MoCExchange'], True))
available_list.append(('MoCInrate', connector_addresses['MoCInrate'], True))
available_list.append(('MoCBurnout', connector_addresses['MoCBurnout'], True))
available_list.append(('DoCToken', connector_addresses['DoCToken'], False))
available_list.append(('BProToken', connector_addresses['BProToken'], False))
available_list.append(('MoCBProxManager', connector_addresses['MoCBProxManager'], True))
available_list.append(('MoCMedianizer', moc_moc.sc_moc_state.price_provider(), False))
available_list.append(('CommissionSplitter', moc_moc.sc_moc_inrate.commission_address(), True))
if is_vendor:
    available_list.append(('MoCOracle', moc_moc.sc_moc_state.moc_price_provider(), False))
    available_list.append(('MoCToken', moc_moc.sc_moc_state.moc_token(), False))
    available_list.append(('MoCVendors', moc_moc.sc_moc_state.moc_vendors(), True))


events_functions = 'Upgraded'
hours_delta = 0
from_block = 1982520  # from block start
to_block = 1982540  # block end or 0 to last block
block_steps = 1000


last_block_number = int(network_manager.block_number)

if to_block <= 0:
    to_block = last_block_number  # last block number in the node

current_block = from_block

l_events = list()
count = 0
while current_block <= to_block:

    step_end = current_block + block_steps
    if step_end > to_block:
        step_end = to_block

    log.info("Scanning blocks steps from {0} to {1}".format(current_block, step_end))

    contract_proxy_admin = ProxyAdminInterface(network_manager,
                                               contract_address=Web3.toChecksumAddress(available_list[0][1]))
    events = contract_proxy_admin.filter_events(from_block=current_block, to_block=step_end)
    if events:
        for event in events:
            if events_functions in event['event']:
                eve = EventUpgradeabilityProxyUpgraded(event)
                print(eve.print_table())
                print()
                l_events.append(eve)

                count += 1

    # Adjust current blocks to the next step
    current_block = current_block + block_steps


# finally disconnect from network
network_manager.disconnect()

duration = time.time() - start_time
log.info("Succesfull!! Done in {0} seconds".format(duration))
