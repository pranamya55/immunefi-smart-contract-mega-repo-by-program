"""
console> brownie networks add RskNetwork rskTestnetLocal2 host=http://localhost:4454 chainid=31 explorer=https://blockscout.com/rsk/mainnet/api

"""

from moneyonchain.networks import network_manager
from moneyonchain.governance import EventUpgradeabilityProxyUpgraded, AdminUpgradeabilityProxy

connection_network = 'rskTestnetLocal2'
config_network = 'mocTestnetAlpha'

# Connect to network
network_manager.connect(
    connection_network=connection_network,
    config_network=config_network)

contract_address = '0x01AD6f8E884ed4DDC089fA3efC075E9ba45C9039'
proxy_contract = AdminUpgradeabilityProxy(network_manager, contract_address=contract_address).from_abi()

events = proxy_contract.filter_events(from_block=2078050, to_block=2078060)
if events:
    for event in events:
        if 'Upgraded' in event['event']:
            eve = EventUpgradeabilityProxyUpgraded(event)
            eve.print_table()

# finally disconnect from network
network_manager.disconnect()
