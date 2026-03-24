"""
To run this script need private key, run this scripts with:

user> export ACCOUNT_PK_SECRET=PK
user> python ./mint.py

Where replace with your PK, and also you need to have funds in this account
"""

from moneyonchain.networks import network_manager
from moneyonchain.tokens import MoCToken

connection_network = 'bscTestnetPrivate'
config_network = 'bnbTestnet'

# Connect to network
network_manager.connect(
    connection_network=connection_network,
    config_network=config_network)


#moc_token_address = '0x73E12fBFae52A39bF0819019a368Eb368Ce15738'
moc_token_address = '0x1C382A7C0481ff75C69EC1757Eff297C9255494B'
beneficiary_account_address = '0xF9f405832140cC723709C94266b3FA02BF9C3F43'
amount = int(60000 * 10 ** 18)
moc_token = MoCToken(network_manager, contract_address=moc_token_address).from_abi()


print("MoC Token address: {0}".format(moc_token_address))
print("Account: {0}".format(beneficiary_account_address))

print("Balances BEFORE")
print("===============")
print("Balance: {0} {1}".format(moc_token.balance_of(beneficiary_account_address), moc_token.symbol()))
#print("Allowance: {0} {1}".format(moc_token.allowance(beneficiary_account_address, moc_address, block_identifier=2292933), moc_token.symbol()))


print("Please wait to the transaction be mined!...")
tx_args = moc_token.tx_arguments()
tx_receipt = moc_token.sc.mint(beneficiary_account_address, amount, tx_args)

print("Balances AFTER")
print("===============")
print("Balance: {0} {1}".format(moc_token.balance_of(beneficiary_account_address), moc_token.symbol()))

# finally disconnect from network
network_manager.disconnect()
