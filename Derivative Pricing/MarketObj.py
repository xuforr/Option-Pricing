# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 21:53:51 2018

@author: Administrator
"""
import pandas as pd

class myMarket:
    def __init__(self):
        self._db = {}
    
    def save_data(self, data, ticker, over_write = False):
        if ticker not in self._db:
            if type(data) is pd.DataFrame:
                if type(data.index[0]) is not pd.Timestamp:
                    new_data = data.copy()
                    new_data.index = [pd.Timestamp(idx) for idx in data.index]
                    data = new_data
            elif type(data) is dict:
                if type(next(iter(data))) is not pd.Timestamp:
                    new_data = {}
                    for key in data:
                        new_data[pd.Timestamp(key)] = data[key]
                    data = new_data
            else:
                raise TypeError('Data type {} is not yet supported!'.format(type(data)))
            self._db[ticker] = data
            print('Market data for {} has been added!'.format(ticker))
        else:
            if over_write:
                print('Over writing {}!'.format(ticker))
            else:
                print('{} already exist!'.format(ticker))
    
    def remove_data(self, ticker):
        if ticker not in self._db:
            print('{} doens\'t exist!'.format(ticker))
        else:
            del self._db[ticker]
            print('Market data for {} has been removed!'.format(ticker))
    
    def get_spot(self, ticker, time_idx):
        if type(time_idx) is not pd.Timestamp:
            try:
                time_idx = pd.Timestamp(time_idx)
            except:
                raise TypeError('Cannot convert {} to timestamp!'.format(time_idx))
        if ticker in self._db:
            try:
                if type(self._db[ticker])is pd.core.frame.DataFrame:
                    return self._db[ticker].loc[time_idx,].values
                else:
                    return self._db[ticker][time_idx]
            except:
                raise ValueError('Market data for {} doesnt\'t exist on {}'.format(ticker, time_idx))
        else:
            raise ValueError('Market data for {} doesn\'t exist!'.format(ticker))

if __name__ == '__main__':
    pass
