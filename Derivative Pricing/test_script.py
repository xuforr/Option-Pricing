# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 22:03:33 2018

@author: Administrator
"""

import DataObj as DO
import TradableObj as TO
import OptionObj as options
import MarketObj as MO
import PayoffObj as PO
import datetime

# Get data from online source
io = DO.myIO()
data = io.read('GS', 'iex', start = datetime.datetime(2017,1,1), end = None)
market = MO.myMarket()
market.save_data(data[['close']], 'GS')

# Get fake data for testing purpose
ir = lambda x: 0.01
iv = lambda x: 0.20
iq = lambda x: 0.0
interest_rate = {}
implied_vol = {}
dividend = {}
for t in data.index:
    interest_rate[t] = ir
    implied_vol[t] = iv
    dividend[t] = iq
market.save_data(interest_rate, 'DOM_IR')
market.save_data(implied_vol, 'GS_IV')
market.save_data(dividend, 'GS_DIV')

# Create securities: Stock, Option
Stock = TO.equity('GS', market)
P1 = PO.payoff(250, datetime.datetime(2018,8,3), True)
Option = options.European_Option('GS_O_C', Stock, P1, market)

# Price option
assert( Option.dollar_price('2017-12-28') > 0 )
assert( Option.dollar_price('2018-8-2') > 0 )