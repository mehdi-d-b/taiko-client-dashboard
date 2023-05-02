# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 09:23:53 2023

@author: MB273828
"""
import param
import redis
import json
from scipy.signal import spectrogram

import holoviews as hv 
import pandas as pd, numpy as np
from holoviews.streams import Pipe
from holoviews import opts

from tornado.ioloop import PeriodicCallback
from tornado import gen

class Spectrogram(param.Parameterized):

    filtre_1 = param.ObjectSelector(
        default="Valeur 1", 
        objects=["Valeur 1", "Valeur 2", "Valeur 3", "Valeur 4"]
    )
    filtre_2 = param.ObjectSelector(
        default="Valeur 2", 
        objects=["Valeur 1", "Valeur 2", "Valeur 3", "Valeur 4"]
    )
    valeur_1 = param.Number(0.0, precedence=0)
        
    # Connect to Redis cache
    r = redis.Redis()
    
    pipe = Pipe(data=[])
    
    @gen.coroutine
    def spec_data(self):
        # Read the last element from the Redis list
        data = [json.loads(x) for x in self.r.lrange('random_sin', 0, -1)]
        sig = [(row["var_0"] + 
                row["var_1"] +
                row["var_2"] +
                row["var_3"] +
                row["var_4"] +
                row["var_5"] +
                row["var_6"] +
                row["var_7"] 
                ) for row in data]    
        xs, ys, zs = spectrogram(np.array(sig), fs=1000)
        self.pipe.send((ys, xs, 10*np.log10(zs)))
    
    def view(self):
        PeriodicCallback(self.spec_data, 1000).start()
        
        return hv.DynamicMap(hv.Image ,streams=[self.pipe]).opts(
             opts.Image(
                title='Spectrogram', 
                tools=['hover'],
                colorbar=True,
                #default_tools = ['save', 'box_zoom', 'reset'],
                cmap='rainbow',
                width=1200, 
                height=600,
                xlim=(0, 1), 
                ylim=(0, 500)
                )
        ).redim.range(z=(-70,0))