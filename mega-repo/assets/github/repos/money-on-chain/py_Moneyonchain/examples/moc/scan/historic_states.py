"""
This is script getting historic data from MOC State contract
16/03/2020
"""

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoCState
from moneyonchain.rdoc import RDOCMoCState

import datetime
import csv
import time

connection_network = 'rskMainnetPublic'
config_network = 'rdocMainnet'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)

if network_manager.options['networks'][config_network]['app_mode'] == 'MoC':
    moc_state = MoCState(network_manager).from_abi()
else:
    moc_state = RDOCMoCState(network_manager).from_abi()

from_block = 3710582  # can be manually setting
to_block = 3710683  # can be manually setting
block_steps = 10000
block_skip = 1
hours_delta = 0
last_block_number = int(network_manager.block_number)
bucket_x2 = moc_state.bucket_x2()
bucket_c0 = moc_state.bucket_c0()

if to_block <= 0:
    to_block = last_block_number  # last block number in the node

current_block = from_block

l_historic_data = list()
print("Getting historic data from MOC/RDOC... Wait please...")
print("Starting Scan Blocks From Block: {0} To Block: {1}".format(from_block, to_block))

start_time = time.time()

while current_block <= to_block:

    step_end = current_block + block_steps
    if step_end > to_block:
        step_end = to_block

    print("Scanning blocks steps from {0} to {1}".format(current_block, step_end))

    for n_block in range(current_block, step_end, block_skip):

        print("Get info from block: {0}".format(n_block))

        ts = network_manager.block_timestamp(n_block)
        dt = ts - datetime.timedelta(hours=hours_delta)
        d_timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")

        d_info_data = dict()

        d_info_data['blockNumber'] = n_block
        d_info_data['Timestamp'] = d_timestamp

        # bitcoin price
        try:
            d_info_data['BTCprice'] = moc_state.bitcoin_price(block_identifier=n_block)
        except:
            print("No price valid in BLOCKHEIGHT: [{0}] skipping!".format(n_block))
            continue

        # Moving average
        d_info_data['EMAvalue'] = moc_state.bitcoin_moving_average(block_identifier=n_block)

        # days to settlement, 0 is the day of the settlement
        d_info_data['daysToSettlement'] = int(moc_state.days_to_settlement(block_identifier=n_block))

        # bkt_0 Storage DOC
        d_info_data['C0_getBucketNDoc'] = moc_state.bucket_ndoc(bucket_c0, block_identifier=n_block)

        # bkt_0 Storage BPro
        d_info_data['C0_getBucketNBPro'] = moc_state.bucket_nbpro(bucket_c0, block_identifier=n_block)

        # bkt_0 Storage BTC
        d_info_data['C0_getBucketNBTC'] = moc_state.bucket_nbtc(bucket_c0, block_identifier=n_block)

        # bkt_0 Storage InrateBag
        d_info_data['C0_getInrateBag'] = moc_state.get_inrate_bag(bucket_c0, block_identifier=n_block)

        # bkt_0 Storage Coverage
        d_info_data['C0_coverage'] = moc_state.coverage(bucket_c0, block_identifier=n_block)

        # bkt_0 Storage Leverage
        d_info_data['C0_leverage'] = moc_state.leverage(bucket_c0, block_identifier=n_block)

        # bkt_2 Storage DOC
        d_info_data['X2_getBucketNDoc'] = moc_state.bucket_ndoc(bucket_x2, block_identifier=n_block)

        # bkt_2 Storage BPro
        d_info_data['X2_getBucketNBPro'] = moc_state.bucket_nbpro(bucket_x2, block_identifier=n_block)

        # bkt_2 Storage BTC
        d_info_data['X2_getBucketNBTC'] = moc_state.bucket_nbtc(bucket_x2, block_identifier=n_block)

        # bkt_2 Inrate Bag
        d_info_data['X2_getInrateBag'] = moc_state.get_inrate_bag(bucket_x2, block_identifier=n_block)

        # bkt_2 Coverage
        d_info_data['X2_coverage'] = moc_state.coverage(bucket_x2, block_identifier=n_block)

        # bkt_2 Storage Leverage
        d_info_data['X2_leverage'] = moc_state.leverage(bucket_x2, block_identifier=n_block)

        # Global Coverage
        d_info_data['globalCoverage'] = moc_state.global_coverage(block_identifier=n_block)

        # Bitpro total supply in system
        d_info_data['bproTotalSupply'] = moc_state.bitpro_total_supply(block_identifier=n_block)

        # All DOC in circulation
        d_info_data['docTotalSupply'] = moc_state.doc_total_supply(block_identifier=n_block)

        # RBTC in sytem
        d_info_data['rbtcInSystem'] = moc_state.rbtc_in_system(block_identifier=n_block)

        # BPro Tec price
        d_info_data['bproTecPrice'] = moc_state.bpro_tec_price(block_identifier=n_block)

        # BTC2X Tec price
        d_info_data['BTC2XTecPrice'] = moc_state.btc2x_tec_price(bucket_x2, block_identifier=n_block)

        l_historic_data.append(d_info_data)

    # Adjust current blocks to the next step
    current_block = current_block + block_steps


# Write list to CSV File

if l_historic_data:
    columns = ['Block Nº',
               'Timestamp',
               'BTCprice',
               'EMAvalue',
               'To Settlement',
               'Bkt_0 NBTC',
               'Bkt_0 NBPro',
               'Bkt_0 NDoc',
               'Bkt_0 Inrate Bag',
               'Bkt_0 Coverage',
               'Bkt_0 Leverage',
               'Bkt_2 NBTC',
               'Bkt_2 NBPro',
               'Bkt_2 NDoc',
               'Bkt_2 Inrate Bag',
               'Bkt_2 Coverage',
               'Bkt_2 Leverage',
               'Global Cov',
               'BPro Total Supply',
               'DOC Total Supply',
               'RBTC in system',
               'BPro Tec. Price',
               'BTC2X Tec. Price'
               ]
    path_file = '{0}_historic_data_{1}_{2}.csv'.format(config_network, from_block, to_block)
    with open(path_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(columns)

        count = 0
        for historic_data in l_historic_data:
            count += 1
            row = [historic_data['blockNumber'],
                   historic_data['Timestamp'],
                   format(historic_data['BTCprice'], '.18f'),
                   format(historic_data['EMAvalue'], '.18f'),
                   historic_data['daysToSettlement'],
                   format(historic_data['C0_getBucketNBTC'], '.18f'),
                   format(historic_data['C0_getBucketNBPro'], '.18f'),
                   format(historic_data['C0_getBucketNDoc'], '.18f'),
                   format(historic_data['C0_getInrateBag'], '.18f'),
                   format(historic_data['C0_coverage'], '.18f'),
                   format(historic_data['C0_leverage'], '.18f'),
                   format(historic_data['X2_getBucketNBTC'], '.18f'),
                   format(historic_data['X2_getBucketNBPro'], '.18f'),
                   format(historic_data['X2_getBucketNDoc'], '.18f'),
                   format(historic_data['X2_getInrateBag'], '.18f'),
                   format(historic_data['X2_coverage'], '.18f'),
                   format(historic_data['X2_leverage'], '.18f'),
                   format(historic_data['globalCoverage'], '.18f'),
                   format(historic_data['bproTotalSupply'], '.18f'),
                   format(historic_data['docTotalSupply'], '.18f'),
                   format(historic_data['rbtcInSystem'], '.18f'),
                   format(historic_data['bproTecPrice'], '.18f'),
                   format(historic_data['BTC2XTecPrice'], '.18f')
                   ]
            writer.writerow(row)

duration = time.time() - start_time
print("Getting historic data from MOC/RDOC done! Succesfull!! Done in {0} seconds".format(duration))

# finally disconnect from network
network_manager.disconnect()
