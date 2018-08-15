# -*- coding: utf-8 -*-
"""
@author: xuforr
"""
import numpy as np
import scipy.stats as ss
import pandas as pd
import datetime

class tradable:
    def __init__(self, market):
        self._market = market
        pass
    
    def dollar_price(self):
        pass
    
class option(tradable):
    def __init__(self, ticker, underlying, payoff):
        """
        type ticker: string
        type underlying: tradable
        type payoff: payoff
        """
        self._payoff = payoff
        self._under = underlying
        self._ticker = ticker
        self._pricing_method = 'default'
        
    def set_pricing_method(self, new_method):
        self._pricing_method = new_method
    
    def dollar_price(self, pricing_method = None):
        pass
    
    def delta(self):
        pass
    
    def gamma(self):
        pass
    
    def theta(self):
        pass
    
    def rho(self):
        pass
    
    def vega(self):
        pass

class European_Option(option):
    def __init__(self, ticker, underlying, payoff, market):
        """
        type ticker: string
        type underlying: tradable
        type payoff: payoff
        """
        self._payoff = payoff
        self._underlier = underlying
        self._ticker = ticker
        self._pricing_method = 'Analytical'
        self._market = market
        
    def dollar_price(self, pricing_date, pricing_method = None):
        if pricing_method:
            self.set_pricing_method(pricing_method)
        if self._pricing_method is 'Analytical':
            return self.Analytical_pricer(pricing_date)
        elif self._pricing_method is 'Grid':
            return None
        elif self._pricing_method is 'Monte Carlo':
            return None
        else:
            raise ValueError('{} pricing is not supported!'.format(self._pricing_method))
            
    def strike(self):
        return self._payoff.strike
    
    def expiration(self):
        return self._payoff.expiration
    
    def implied_vol(self, pricing_date):
        iv_func = self._market.get_spot(self._underlier.get_ticker()+'_IV', pricing_date)
        return iv_func(self._payoff.strike)
    
    def _get_inputs(self, pricing_date):
        # Inputs from contract payoff
        K = self._payoff.strike
        T = self._payoff.expiration        
        # Inputs from underlier
        S = self._underlier.spot(pricing_date)
        q = self._underlier.dividend(pricing_date)
        # Inputs from market
        r_func = self._market.get_spot('DOM_IR', pricing_date)
        r = r_func(T)
        iv = self.implied_vol(pricing_date)
        if pricing_date is not pd.Timestamp:
            pricing_date = pd.Timestamp(pricing_date)
        dt = (T - pricing_date)/datetime.timedelta(days = 365)
        return S, K, r, q, dt, iv
    
    def Analytical_pricer(self, pricing_date):
        S, K, r, q, dt, iv = self._get_inputs(pricing_date)
        # Pricing formula
        d1 = (np.log(S/K) + (r-q)*dt + iv**2 * dt/2) /iv * np.sqrt(dt)
        d2 = (np.log(S/K) + (r-q)*dt - iv**2 * dt/2) /iv * np.sqrt(dt)
        if self._payoff.call:
            return np.exp(-q*dt)*S*ss.norm.cdf(d1) - np.exp(-r*dt)*K*ss.norm.cdf(d2)
        else:
            return np.exp(-r*dt)*K*ss.norm.cdf(-d2) - np.exp(-q*dt)*S*ss.norm.cdf(-d1)
    
    def delta(self, pricing_date):
        S, K, r, q, dt, iv = self._get_inputs(pricing_date)
        # Pricing formula
        d1 = (np.log(S/K) + (r-q)*dt + iv**2 * dt/2) /iv * np.sqrt(dt)
        #d2 = (np.log(S/K) + (r-q)*dt - iv**2 * dt/2) /iv * np.sqrt(dt)
        if self._payoff.call:
            return np.exp(-q*dt) * ss.norm.cdf(d1)
        else:
            return -np.exp(-q*dt) * ss.norm.cdf(-d1)
        
    def gamma(self, pricing_date):
        S, K, r, q, dt, iv = self._get_inputs(pricing_date)
        # Pricing formula
        d1 = (np.log(S/K) + (r-q)*dt + iv**2 * dt/2) /iv * np.sqrt(dt)
        #d2 = (np.log(S/K) + (r-q)*dt - iv**2 * dt/2) /iv * np.sqrt(dt)
        return S*np.exp(-q*dt)*ss.norm.pdf(d1)/(S*iv*np.sqrt(dt))

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

