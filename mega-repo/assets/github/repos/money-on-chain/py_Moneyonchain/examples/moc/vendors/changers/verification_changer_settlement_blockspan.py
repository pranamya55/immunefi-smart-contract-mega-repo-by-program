from moneyonchain.networks import network_manager
from moneyonchain.moc_vendors import MoCSettlementChanger


import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/changers_settlement_blockspan.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnet'


# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

# changer contract address
changer_address = '0x614a029B926f87CaA47a2c658C2f3B08c74694dB'

contract_changer = MoCSettlementChanger(network_manager, contract_address=changer_address).from_abi()

print("Block span to change: {0}".format(contract_changer.block_span()))

# finally disconnect from network
network_manager.disconnect()
