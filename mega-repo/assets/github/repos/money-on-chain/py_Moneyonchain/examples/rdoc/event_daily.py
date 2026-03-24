import datetime
from web3 import Web3
from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCMoCInrate, RDOCMoC

connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


moc_inrate = RDOCMoCInrate(network_manager).from_abi()

events_functions = ['InrateDailyPay']
hours_delta = 0
from_block = 830859  # from block start
to_block = 844859  # block end or 0 to last block
l_events = moc_inrate.logs_from(events_functions, from_block, to_block, block_steps=2880)

l_info = list()
if 'InrateDailyPay' in l_events:
    if l_events['InrateDailyPay']:
        count = 0
        for e_event_block in l_events['InrateDailyPay']:
            for e_event in e_event_block:

                count += 1
                ts = network_manager.block_timestamp(e_event['blockNumber'])
                dt = ts - datetime.timedelta(hours=hours_delta)
                d_timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")

                d_info = dict()
                d_info['blockNumber'] = e_event['blockNumber']
                d_info['timestamp'] = d_timestamp
                d_info['amount'] = Web3.fromWei(e_event['args']['amount'], 'ether')
                d_info['daysToSettlement'] = e_event['args']['daysToSettlement']
                d_info['nReserveBucketC0'] = Web3.fromWei(e_event['args']['nReserveBucketC0'], 'ether')

                l_info.append(d_info)

print(l_info)

network_manager.disconnect()
