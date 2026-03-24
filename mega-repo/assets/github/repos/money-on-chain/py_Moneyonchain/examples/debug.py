"""
"""

from web3 import Web3

#from moneyonchain.networks import network_manager, web3
#from moneyonchain.transaction import TransactionReceipt

connection_network = 'rskMainnetLocal2'
config_network = 'mocMainnet2'

# Connect to network
#network_manager.connect(connection_network=connection_network, config_network=config_network)

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:4454', request_kwargs={'timeout': 300}))
print(w3.manager.request_blocking('debug_traceTransaction', ["0x6ffabe8da76e70bf6cb31c4041380fe1be5fad9b129ad29d2942a2f9e6653ab8"]))

"""
curl \
    -X POST \
    -H "Content-Type:application/json" \
    --data '{"jsonrpc":"2.0","method":"debug_traceTransaction","params":["0x4e9d143b95d5a1611b027aa98ee8e15aeb1c52a30fbc65f3d2980af68a75f0f2"],"id":1}' \
    http://127.0.0.1:4454
"""