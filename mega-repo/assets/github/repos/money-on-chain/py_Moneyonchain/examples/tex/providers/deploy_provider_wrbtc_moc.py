"""
Deploy Price Provider WRBTC/MoC
"""

from moneyonchain.networks import network_manager
from moneyonchain.tex import TexMocBtcPriceProviderFallback

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='logs/deploy_provider_wrbtc_moc.log',
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
config_network = 'dexMainnet'

# Connect to network
network_manager.connect(connection_network=connection_network, config_network=config_network)

# base_token = '0x09b6ca5E4496238A1F176aEa6Bb607DB96c2286E'  # WRBTC
# secondary_token = '0x0399c7F7B37E21cB9dAE04Fb57E24c68ed0B4635'  # AMOC
# moc_state = '0x0adb40132cB0ffcEf6ED81c26A1881e214100555'
# base_token_doc_moc = '0x489049c48151924c07F86aa1DC6Cc3Fea91ed963'  # ADOC
# secondary_token_doc_moc = '0x0399c7F7B37E21cB9dAE04Fb57E24c68ed0B4635'  # AMOC

# base_token = '0x09b6ca5E4496238A1F176aEa6Bb607DB96c2286E'  # WRBTC
# secondary_token = '0x45a97b54021a3F99827641AFe1BFAE574431e6ab'  # MOC
# moc_state = '0x0adb40132cB0ffcEf6ED81c26A1881e214100555'
# base_token_doc_moc = '0xCB46c0ddc60D18eFEB0E586C17Af6ea36452Dae0'  # DOC
# secondary_token_doc_moc = '0x45a97b54021a3F99827641AFe1BFAE574431e6ab'  # MOC

base_token = '0x967f8799aF07DF1534d48A95a5C9FEBE92c53ae0'  # WRBTC
secondary_token = '0x9AC7fE28967B30E3A4e6e03286d715b42B453D10'  # MOC
moc_state = '0xb9C42EFc8ec54490a37cA91c423F7285Fa01e257'
base_token_doc_moc = '0xe700691dA7b9851F2F35f8b8182c69c53CcaD9Db'  # DOC
secondary_token_doc_moc = '0x9AC7fE28967B30E3A4e6e03286d715b42B453D10'  # MOC


log.info("Deploying in network: {0}".format(config_network))
log.info("base_token: {0}".format(base_token))
log.info("secondary_token: {0}".format(secondary_token))
log.info("moc_state: {0}".format(moc_state))
log.info("base_token_doc_moc: {0}".format(base_token_doc_moc))
log.info("secondary_token_doc_moc: {0}".format(secondary_token_doc_moc))

price_provider = TexMocBtcPriceProviderFallback(network_manager)
tx_receipt = price_provider.constructor(
    moc_state,
    base_token,
    secondary_token,
    base_token_doc_moc,
    secondary_token_doc_moc)

if tx_receipt:
    log.info("Price provider deployed Contract Address: {address}".format(address=tx_receipt.contract_address))
else:
    log.info("Error deploying price provider")

# finally disconnect from network
network_manager.disconnect()
