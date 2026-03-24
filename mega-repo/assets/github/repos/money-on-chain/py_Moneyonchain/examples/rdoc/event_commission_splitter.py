import datetime
from web3 import Web3
from moneyonchain.networks import network_manager
from moneyonchain.rdoc import RDOCCommissionSplitter


connection_network = 'rskMainnetPublic'
config_network = 'rdocMainnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


splitter = RDOCCommissionSplitter(network_manager).from_abi()

events_functions = ['SplitExecuted']
hours_delta = 0
from_block = 2209643  # from block start
to_block = 2329643  # block end or 0 to last block
l_events = splitter.logs_from(events_functions, from_block, to_block, block_steps=2880)

l_info = list()
if 'SplitExecuted' in l_events:
    if l_events['SplitExecuted']:
        count = 0
        for e_event_block in l_events['SplitExecuted']:
            for e_event in e_event_block:

                count += 1
                ts = network_manager.block_timestamp(e_event['blockNumber'])
                dt = ts - datetime.timedelta(hours=hours_delta)
                d_timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")

                d_info = dict()
                d_info['blockNumber'] = e_event['blockNumber']
                d_info['timestamp'] = d_timestamp
                d_info['commissionAmount'] = Web3.fromWei(e_event['args']['commissionAmount'], 'ether')
                d_info['mocAmount'] = Web3.fromWei(e_event['args']['mocAmount'], 'ether')

                l_info.append(d_info)

print(l_info)

# finally disconnect from network
network_manager.disconnect()
