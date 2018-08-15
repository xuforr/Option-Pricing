# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 21:52:48 2018

@author: Administrator
"""

import pandas as pd
import quandl

class myIO:
    def __init__(self):
        self._quandl_key = 'DDaF-AHmkSuzDSrPBU6k'
        self._local_dir = ''
        quandl.ApiConfig.api_key = self._quandl_key
        
    def read(self, ticker, *source, **kwargs):
        if source[0] == 'local':
            data = pd.read_csv(ticker, **kwargs)
        else:
            data = quandl.get(ticker, **kwargs)
        return data
    
    def save(self, obj, file_name, path = '', **kwargs):
        if path == '':
            path = self._local_dir
        save_to = '{}/{}'.format(path, file_name)
        if type(obj) is pd.core.frame.DataFrame:
            obj.to_csv(save_to, **kwargs)
        elif file_name.endswith('png'):
            obj.savefig(save_to)
            
if __name__ == '__main__':
    assert( myIO() is not None )
                