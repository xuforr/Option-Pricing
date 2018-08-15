# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 22:11:33 2018

@author: Administrator
"""

class payoff:
    def __init__(self, strike, expiration, call):
        self.strike = strike
        self.expiration = expiration
        self.call = call