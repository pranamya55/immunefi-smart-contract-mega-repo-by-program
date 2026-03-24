from rich.console import Console
from rich.table import Table

from moneyonchain.networks import NetworkManager
from moneyonchain.tex import MoCDecentralizedExchange, CommissionManager

console = Console()

connection_network='rskTesnetPublic'
config_network = 'dexTestnet'

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


dex = MoCDecentralizedExchange(network_manager).from_abi()
dex_commission = CommissionManager(network_manager).from_abi()

table = Table(show_header=True, header_style="bold magenta", title="Contracts network: {0}".format(config_network))
table.add_column("Contract")
table.add_column("Proxy")
table.add_column("Implementation")

lib_address = network_manager.options['networks'][config_network]['addresses']['MoCExchangeLib']
rows = list()
rows.append(('MoCDecentralizedExchange', dex.address(), dex.implementation()))
rows.append(('CommissionManager', dex_commission.address(), dex_commission.implementation()))
rows.append(('MoCExchangeLib', lib_address, lib_address))

for row in rows:
    table.add_row(
        row[0], row[1], row[2]
    )

console.print(table)


if config_network in 'dexMainnet':
    link_explorer = 'https://explorer.rsk.co/address/{0}'
elif config_network in 'dexTestnet':
    link_explorer = 'https://explorer.testnet.rsk.co/address/{0}'
else:
    link_explorer = 'https://explorer.rsk.co/address/{0}'

md_header = '''
| Contract                      | Proxy                           | Implementation                 |
| :---------------------------- | -----------------------------   | ------------------------------ |'''

md_lines = list()
for row in rows:
    line = '| {0} | [{1}]({2}) | [{3}]({4}) | '.format(row[0],
                                                       row[1], link_explorer.format(row[1]),
                                                       row[2], link_explorer.format(row[2]))
    md_lines.append(line)

print(md_header)
print('\n'.join(md_lines))


# finally disconnect from network
network_manager.disconnect()
