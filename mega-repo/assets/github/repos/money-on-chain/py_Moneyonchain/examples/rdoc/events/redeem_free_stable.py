"""

Buyer Match event

"""

import time
import csv
import os

from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoCExchange, MoCExchangeFreeStableTokenRedeem


import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/redeem_free_stable.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network = 'rskMainnetLocal2'
config_network = 'rdocMainnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

log.info("Starting to import events from contract...")
start_time = time.time()

# RDOCMoCExchange.sol
exchange = RDOCMoCExchange(network_manager).from_abi()

events_functions = 'FreeStableTokenRedeem'
hours_delta = 0
from_block = 3911450  # from block start
to_block = 3911460  # block end or 0 to last block
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

    events = exchange.filter_events(from_block=current_block, to_block=step_end)
    if events:
        for event in events:
            if events_functions in event['event']:
                eve = MoCExchangeFreeStableTokenRedeem(event)
                print(eve.print_table())
                print()
                l_events.append(eve)

                count += 1

    # Adjust current blocks to the next step
    current_block = current_block + block_steps

# # Write list to CSV File
#
if l_events:
    columns = MoCExchangeFreeStableTokenRedeem.columns()
    path_file = '{0}_free_stable_{1}_{2}.csv'.format(config_network, from_block, to_block)
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
log.info("Succesfull!! Done in {0} seconds".format(duration))
