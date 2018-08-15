# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 22:03:33 2018

@author: Administrator
"""

import DataObj as DO
import TradableObj as TO
import MarketObj as MO
import PayoffObj as PO
import datetime

io = DO.myIO()
cny = io.read('FED/RXI_N_B_CH', 'quandl', start_date = '2017-12-31', end_date = '2018-08-09')
market = MO.myMarket()
market.save_data(cny, 'USD_CNY')

ir = lambda x: 0.01
iv = lambda x: 0.25
iq = lambda x: 0.0
interest_rate = {}
implied_vol = {}
dividend = {}
for t in cny.index:
    interest_rate[t] = ir
    implied_vol[t] = iv
    dividend[t] = iq
market.save_data(interest_rate, 'DOM_IR')
market.save_data(implied_vol, 'USD_CNY_IV')
market.save_data(dividend, 'USD_CNY_DIV')

USD_CNY = TO.equity('USD_CNY', market)
P1 = PO.payoff(6.5, datetime.datetime(2018,12,31), True)
O_UDCN = TO.European_Option('O_UDCN', USD_CNY, P1, market)
print(O_UDCN.dollar_price('2018-01-12'))