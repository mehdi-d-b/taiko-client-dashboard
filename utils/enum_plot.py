# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 09:23:53 2023

@author: MB273828
"""
import param
import redis
import json

import holoviews as hv 
import pandas as pd, numpy as np
from holoviews.streams import Buffer

from tornado.ioloop import PeriodicCallback
from tornado import gen


INITIAL_DATA = pd.DataFrame(
    {
        "timestamp": np.array([]),
        "enum": np.array([])
    }
)
INITIAL_DATA.set_index("timestamp", inplace=True)


class EnumPlot(param.Parameterized):
        
    r = redis.Redis()
    
    buffer = Buffer(data=INITIAL_DATA, length=1000)

    @gen.coroutine
    def enum_data(self):
        # Read the last element from the Redis list
        data = self.r.lindex('random_sin', -1)
        if data:
            data = json.loads(data)
            index = pd.to_datetime(data['timestamp'], unit='ms')
            data = pd.DataFrame({
                               'timestamp': [index],
                               'enum': [data['enum']]})
            self.buffer.send(data)


    

    def enum_curves(self, data: pd.DataFrame):
        data = data.sort_values(by="timestamp").tail(1000)              
        return (
            hv.Curve(data[["timestamp", "enum"]], label="Enumérateur")
        )

    def view(self):
        PeriodicCallback(self.enum_data, 100).start()
        return hv.DynamicMap(self.enum_curves, streams=[self.buffer]).opts(
            responsive=True, height=250, title="Enumérateur", tools=["hover"]
        )
