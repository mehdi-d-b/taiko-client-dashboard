import param
import json
from datetime import datetime, timedelta
import math

import holoviews as hv 
import pandas as pd, numpy as np
from holoviews.streams import Buffer
from holoviews import opts

from tornado.ioloop import PeriodicCallback
from tornado import gen


INITIAL_DATA = pd.DataFrame(
    {
        "timestamp": np.array([]),
        "channel_1": np.array([]),
        "channel_2": np.array([]),
        "channel_3": np.array([]),
        "channel_4": np.array([])
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
                
        PeriodicCallback(self.get_data, 500).start()

    @gen.coroutine
    def get_data(self):
        timestamps = [datetime.now() - timedelta(milliseconds=100*i) for i in range(5)]
        data = pd.DataFrame(
           {
               "timestamp": timestamps,
                "channel_1": [math.sin(ts.timestamp() * 0.9) * 10 + np.random.normal(0, 0.1) for ts in timestamps],
                "channel_2": [math.sin(ts.timestamp() * 0.8) * 11 + np.random.normal(0, 0.1) for ts in timestamps],
                "channel_3": [math.sin(ts.timestamp() * 0.7) * 12 + np.random.normal(0, 0.1) for ts in timestamps],
                "channel_4": [math.sin(ts.timestamp() / 0.6) * 13 + np.random.normal(0, 0.1) for ts in timestamps],
        }
        )
        data.set_index("timestamp", inplace=True)
        self.value.send(data)

class Sensor(param.Parameterized):
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

    @param.depends("sub1", "sub2", "sub3", "sub4", "offset_1", "offset_2", "offset_3", "offset_4")
    def sin_curves(self, data: pd.DataFrame):
        data = data.sort_values(by="timestamp").tail(300)
        # use the object selectors to subtract the selected channel from the other channels with an offset, lower() is used to convert the channel name to lowercase and replace the underscore with a space
        if self.sub1.lower() != "n/a":
            data["channel_1"] = data["channel_1"] - data[self.sub1.lower().replace(" ", "_")] + self.offset_1
        if self.sub2.lower() != "n/a":
            data["channel_2"] = data["channel_2"] - data[self.sub2.lower().replace(" ", "_")] + self.offset_2
        if self.sub3.lower() != "n/a":
            data["channel_3"] = data["channel_3"] - data[self.sub3.lower().replace(" ", "_")] + self.offset_3
        if self.sub4.lower() != "n/a":
            data["channel_4"] = data["channel_4"] - data[self.sub4.lower().replace(" ", "_")] + self.offset_4   
        
        return (
            hv.Curve(data[["timestamp", "channel_1"]], label="Channel 1")
            * hv.Curve(data[["timestamp", "channel_2"]], label="Channel 2")
            * hv.Curve(data[["timestamp", "channel_3"]], label="Channel 3")
            * hv.Curve(data[["timestamp", "channel_4"]], label="Channel 4")
        )

    def view(self):
        return hv.DynamicMap(self.sin_curves, streams=[self.buffer.value]).opts(
            responsive=True, 
            height=600,
            title="Sensor data", 
            legend_position='top_left'
        ).opts(
            opts.Curve(
                tools=['vline'],
            )
        )
