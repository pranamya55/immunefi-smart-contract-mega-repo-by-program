from decimal import Decimal
import math
from web3 import Web3

from moneyonchain.networks import network_manager
from moneyonchain.moc import MoCInrate


connection_network = 'rskTestnetPublic'
config_network = 'mocTestnetAlpha'

# connection network is the brownie connection network
# config network is our enviroment we want to connect
network_manager.connect(connection_network=connection_network, config_network=config_network)


moc_inrate = MoCInrate(network_manager).from_abi()

"""
Commissions
"""
print("Commission rate: {0}".format(moc_inrate.commision_rate()))


"""
0.25% Annual
"""

print("Bitpro rate: {0}".format(moc_inrate.bitpro_rate()))
print("Bitpro holders interest: {0}".format(moc_inrate.calc_bitpro_holders_interest()))
print("Bitpro interest address: {0}".format(moc_inrate.bitpro_interest_address()))
print("Bitpro interest block span: {0}".format(moc_inrate.bitpro_interest_blockspan()))
print("Bitpro interest last payed block: {0}".format(moc_inrate.last_bitpro_interest_block()))


# amount = Decimal(0.00001)
# print("Daily inrate: {0}".format(moc_inrate.daily_inrate()))
#
# commission = moc_inrate.calc_commission_value(amount)
# mint_interest = moc_inrate.calc_mint_interest_value(amount)
# mint_interest2 = moc_inrate.calc_mint_interest_value(amount, formatted=False)
# print("Interest: {:.22f}".format(mint_interest2))
#
# print("Amount to mint: {:.18f}".format(amount))
# print("Calc commission value: {:.18f}".format(commission))
# print("Calc mint interest value: {:.18f}".format(mint_interest))
# print("RBTC Need it: {:.18f}".format(amount + commission + mint_interest))
# print("RBTC Need it: {0}".format((amount + commission + mint_interest) * 10 ** 18))
# print("RBTC Need it: {0}".format(int(math.ceil((amount + commission + mint_interest) * 10 ** 18))))
# print("RBTC Need it: {0}".format(int(math.ceil((amount + commission + mint_interest + mint_interest*Decimal(0.01)) * 10 ** 18))))
#
# print("To wei {0}".format(Web3.toWei(amount + commission + mint_interest, 'ether')))
# #print("To wei {0}".format(moc_inrate.calc_mint_interest_value2(amount, formatted=False)))
#
# #price = Web3.fromWei(price, 'ether')
# #price = Web3.toInt(result[0])


# finally disconnect from network
network_manager.disconnect()

