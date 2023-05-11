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
        "var_3": np.array([])
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
                               'var_3': [data['var_3']]})
            self.value.send(data)


class Frequencemetre(param.Parameterized):
    sub1 = param.ObjectSelector(
        default="N/A",
        objects=["N/A", "Channel 1", "Channel 2", "Channel 3", "Channel 4"],
        doc="Subtraction for Channel 1"
    )
    sub2 = param.ObjectSelector(
        default="N/A",
        objects=["N/A", "Channel 1", "Channel 2", "Channel 3", "Channel 4"],
        doc="Subtraction for Channel 2"
    )
    sub3 = param.ObjectSelector(
        default="N/A",
        objects=["N/A", "Channel 1", "Channel 2", "Channel 3", "Channel 4"],
        doc="Subtraction for Channel 3"
    )
    sub4 = param.ObjectSelector(
        default="N/A",
        objects=["N/A", "Channel 1", "Channel 2", "Channel 3", "Channel 4"],
        doc="Subtraction for Channel 4"
    )
    offset_1 = param.Number(0.0, precedence=0)
    offset_2 = param.Number(0.0, precedence=0)
    offset_3 = param.Number(0.0, precedence=0)
    offset_4 = param.Number(0.0, precedence=0)
    buffer = param.ClassSelector(class_=SharedBuffer, precedence=-1)

    @param.depends("sub1", "sub2", "sub3", "sub4", "offset_1", "offset_2", "Offset 3", "offset_4")
    def sin_curves(self, data: pd.DataFrame):
        data = data.sort_values(by="timestamp").tail(300)
        # if sub1 = "N/A" 

        
        return (
            hv.Curve(data[["timestamp", "var_0"]], label="Variable 0")
            * hv.Curve(data[["timestamp", "var_1"]], label="Variable 1")
            * hv.Curve(data[["timestamp", "var_2"]], label="Variable 2")
            * hv.Curve(data[["timestamp", "var_3"]], label="Variable 3")
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
