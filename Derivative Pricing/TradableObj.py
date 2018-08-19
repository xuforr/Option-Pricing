# -*- coding: utf-8 -*-
"""
@author: xuforr
"""

class tradable:
    def __init__(self, market):
        self._market = market
        pass
    
    def dollar_price(self):
        pass
    
class equity(tradable):
    def __init__(self, ticker, market):
        """
        type ticker: string
        """
        self._ticker = ticker
        self._market = market
    
    def get_ticker(self):
        return self._ticker
        
    def spot(self, date):
        return self._market.get_spot(self._ticker, date)
    
    def dividend(self, date):
        try:
            self._market.get_spot(self._ticker+'_DIV')
        except:
            return 0.0
    
    dollar_price = spot

