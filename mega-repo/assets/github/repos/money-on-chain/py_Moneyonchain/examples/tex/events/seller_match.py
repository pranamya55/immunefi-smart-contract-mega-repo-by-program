"""

Dex Events

"""

import time
import csv
import os

from moneyonchain.networks import NetworkManager
from moneyonchain.tex import MoCDecentralizedExchange, DEXSellerMatch

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/buyer_match.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network='rskMainnetLocal2'
config_network = 'dexMainnet'

# init network manager
# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager = NetworkManager(
    connection_network=connection_network,
    config_network=config_network)

# run install() if is the first time and you want to install
# networks connection from brownie
# network_manager.install()

# Connect to network
network_manager.connect()

log.info("Starting to import events from contract...")
start_time = time.time()

# MoCDecentralizedExchange.sol
dex = MoCDecentralizedExchange(network_manager).from_abi()

events_functions = 'SellerMatch'
hours_delta = 0
from_block = 3617770  # from block start
to_block = 3638825  # block end or 0 to last block
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

    events = dex.filter_events(from_block=current_block, to_block=step_end)
    if events:
        for event in events:
            if events_functions in event['event']:
                eve = DEXSellerMatch(event)
                print(eve.print_table())
                print()
                l_events.append(eve)

                count += 1

    # Adjust current blocks to the next step
    current_block = current_block + block_steps


# Write list to CSV File

if l_events:
    columns = DEXSellerMatch.columns()
    path_file = '{0}_seller_match_{1}_{2}.csv'.format(config_network, from_block, to_block)
    with open(os.path.join('csv', path_file), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(columns)

        count = 0
        for event in l_events:
            count += 1
            writer.writerow(event.row())

# finally disconnect from network
network_manager.disconnect()

duration = time.time() - start_time
print("Getting events from DEX done! Succesfull!! Done in {0} seconds".format(duration))
