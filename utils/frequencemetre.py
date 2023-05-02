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
from holoviews import opts

from tornado.ioloop import PeriodicCallback
from tornado import gen


INITIAL_DATA = pd.DataFrame(
    {
        "timestamp": np.array([]),
        "var_0": np.array([]),
        "var_1": np.array([]),
        "var_2": np.array([]),
        "var_3": np.array([]),
        "var_4": np.array([]),
        "var_5": np.array([]),
        "var_6": np.array([]),
        "var_7": np.array([]),
    }
)
INITIAL_DATA.set_index("timestamp", inplace=True)


class SharedBuffer(param.Parameterized):
    value = param.ClassSelector(class_=Buffer)
    last_update = param.Date()

    def __init__(self, **params):
        params.update(
            value = Buffer(data=INITIAL_DATA, length=1000),
            last_update = pd.Timestamp.now(),
        )
        super().__init__(**params)
        
        self.r = redis.Redis()
        
        PeriodicCallback(self.sin_data, 100).start()

    @gen.coroutine
    def sin_data(self):
        # Read the last element from the Redis list
        data = self.r.lindex('random_sin', -1)
        if data:
            data = json.loads(data)
            index = pd.to_datetime(data['timestamp'], unit='ms')
            data = pd.DataFrame({
                               'timestamp': [index],
                               'var_0': [data['var_0']],
                               'var_1': [data['var_1']],
                               'var_2': [data['var_2']],
                               'var_3': [data['var_3']],
                               'var_4': [data['var_4']],
                               'var_5': [data['var_5']],
                               'var_6': [data['var_6']],
                               'var_7': [data['var_7']]})
            self.value.send(data)


class Frequencemetre(param.Parameterized):
    c1 = param.ObjectSelector(
        default="Channel 1",
        objects=["N/A", "Channel 1", "Channel 2", "Channel 3", "Channel 4"],
        doc="left side of the subtraction"
    )
    c2 = param.ObjectSelector(
        default="N/A",
        objects=["N/A", "Channel 1", "Channel 2", "Channel 3", "Channel 4"],
        doc="right side of the subtraction",
    )
    offset = param.Number(0.0, precedence=0)
    buffer = param.ClassSelector(class_=SharedBuffer, precedence=-1)

    @param.depends("c1", "c2", "offset")
    def sin_curves(self, data: pd.DataFrame):
        """This function is called from my hv.DynamicMap and plots 8 curves
        I apply my transformation here, on the 8th curve, not elegant but I don't know if there's a better way"""
        data = data.sort_values(by="timestamp").tail(1000)
        
        if self.c1 == "N/A":
            left = 0
        else:
            left = data["var_" + str(self.c1[-1])]
        if self.c2 == "N/A":
            right = 0
        else:
            right = data["var_" + str(self.c2[-1])]
        
        data["var_7"] = (left - right + self.offset)
        
        return (
            hv.Curve(data[["timestamp", "var_0"]], label="Variable 0")
            * hv.Curve(data[["timestamp", "var_1"]], label="Variable 1")
            * hv.Curve(data[["timestamp", "var_2"]], label="Variable 2")
            * hv.Curve(data[["timestamp", "var_3"]], label="Variable 3")
            * hv.Curve(data[["timestamp", "var_4"]], label="Variable 4")
            * hv.Curve(data[["timestamp", "var_5"]], label="Variable 5")
            * hv.Curve(data[["timestamp", "var_6"]], label="Variable 6")
            * hv.Curve(data[["timestamp", "var_7"]], label="Variable 7")
        )

    def view(self):
        return hv.DynamicMap(self.sin_curves, streams=[self.buffer.value]).opts(
            responsive=True, 
            height=600,
            title="Sinusoides", 
            legend_position='top_left'
        ).opts(
            opts.Curve(
                tools=['vline'],
            )
        )
