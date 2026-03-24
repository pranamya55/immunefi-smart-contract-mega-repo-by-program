import datetime
import pprint

from moneyonchain.manager import ConnectionManager
from moneyonchain.moc import FeedFactory

pp = pprint.PrettyPrinter(indent=4)

network = 'mocTestnet'
connection_manager = ConnectionManager(network=network)
print("Connecting to %s..." % network)
print("Connected: {conectado}".format(conectado=connection_manager.is_connected))

moc_feedfactory = FeedFactory(connection_manager)

events_functions = ['Created']
hours_delta = 0
from_block = 166216  # from block start
to_block = 530700  # block end or 0 to last block
l_events = moc_feedfactory.logs_from(events_functions, from_block, to_block, block_steps=2880)

l_info = list()
if 'Created' in l_events:
    if l_events['Created']:
        count = 0
        for e_event_block in l_events['Created']:
            for e_event in e_event_block:

                count += 1
                ts = connection_manager.block_timestamp(e_event['blockNumber'])
                dt = ts - datetime.timedelta(hours=hours_delta)
                d_timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")

                d_info = dict()
                d_info['blockNumber'] = e_event['blockNumber']
                d_info['timestamp'] = d_timestamp
                d_info['sender'] = e_event['args']['sender']
                d_info['feed'] = e_event['args']['feed']

                l_info.append(d_info)
                pp.pprint(d_info)

print("Finish successfully!")
"""

"""