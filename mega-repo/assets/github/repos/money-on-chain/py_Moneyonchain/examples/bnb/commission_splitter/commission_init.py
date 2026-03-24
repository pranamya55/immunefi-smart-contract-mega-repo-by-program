from moneyonchain.networks import network_manager
from moneyonchain.moc import CommissionSplitter

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/commission_init.log',
                    filemode='a')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
console.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(console)


connection_network = 'bscTestnetPrivate'
config_network = 'bnbTestnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

commission = CommissionSplitter(network_manager, contract_address='0x5F1984BdFB81EbA96E95693a08Aec4B5C853Da0C').from_abi()

tx_args = commission.tx_arguments()

moc_address = '0x80cBD706D1Db7840736C34F5177ADEf847f338Cc'
commission_address = '0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3'
proportion = 200000000000000000
governor = '0x236796E659B89af7b466f30cD61051d0Ccb52564'
moc_token = '0x73E12fBFae52A39bF0819019a368Eb368Ce15738'
moc_token_commission = '0xCD8A1c9aCc980ae031456573e34dC05cD7daE6e3'

tx_receipt = commission.sc.initialize(moc_address, commission_address, proportion, governor, moc_token, moc_token_commission, tx_args)

# finally disconnect from network
network_manager.disconnect()



