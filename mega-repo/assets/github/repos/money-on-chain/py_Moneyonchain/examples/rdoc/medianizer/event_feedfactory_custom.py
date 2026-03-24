import datetime
from web3 import Web3
from moneyonchain.networks import network_manager
from moneyonchain.medianizer import RDOCFeedFactory

connection_network = 'rskTestnetPublic'
config_network = 'rdocTestnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)


contract_address_feedfactory = '0xbB26D11bd2a9F2274cD1a8E571e5A352816acaEA'
moc_feedfactory = RDOCFeedFactory(network_manager, contract_address=contract_address_feedfactory).from_abi()

events_functions = ['Created']
hours_delta = 0
from_block = 863000  # from block start
to_block = 863851  # block end or 0 to last block
l_events = moc_feedfactory.logs_from(events_functions, from_block, to_block, block_steps=2880)

l_info = list()
if 'Created' in l_events:
    if l_events['Created']:
        count = 0
        for e_event_block in l_events['Created']:
            for e_event in e_event_block:

                count += 1
                ts = network_manager.block_timestamp(e_event['blockNumber'])
                dt = ts - datetime.timedelta(hours=hours_delta)
                d_timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")

                d_info = dict()
                d_info['blockNumber'] = e_event['blockNumber']
                d_info['timestamp'] = d_timestamp
                d_info['sender'] = e_event['args']['sender']
                d_info['feed'] = e_event['args']['feed']

                l_info.append(d_info)

print(l_info)

# finally disconnect from network
network_manager.disconnect()
