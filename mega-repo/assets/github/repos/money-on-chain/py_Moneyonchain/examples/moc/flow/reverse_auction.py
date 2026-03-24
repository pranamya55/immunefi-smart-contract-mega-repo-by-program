from decimal import Decimal

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoCInrate, CommissionSplitter

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/reverse_auction.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network = 'rskMainnetPublic'
config_network = 'mocMainnet2'

log.info('Connecting enviroment {0}...'.format(config_network))

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

moc_inrate = MoCInrate(network_manager).from_abi()

# get splitter from commission address
commission_address = moc_inrate.commission_address()

log.info("Current commission address (splitter): [{0}]".format(commission_address))

splitter = CommissionSplitter(network_manager, contract_address=commission_address).from_abi()

log.info("Splitter address: [{0}]".format(commission_address))
log.info("Multisig address: [{0}] <- ReverseAuction-BTC2MOC".format(splitter.commission_address()))
log.info("MoC address: [{0}]".format(splitter.moc_address()))
log.info("Splitter balance: [{0}] RBTC".format(splitter.balance()))
log.info("Bitpro interest address: [{0}] <- ReverseAuction-BTC2MOC".format(moc_inrate.bitpro_interest_address()))

# finally disconnect from network
network_manager.disconnect()
