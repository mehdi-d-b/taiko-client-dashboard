import param
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
    channel_1_subtraction = param.ObjectSelector(
        default="N/A",
        objects=["N/A", "Channel 1", "Channel 2", "Channel 3", "Channel 4"],
        doc="Subtraction for Channel 1"
    )
    channel_2_subtraction = param.ObjectSelector(
        default="N/A",
        objects=["N/A", "Channel 1", "Channel 2", "Channel 3", "Channel 4"],
        doc="Subtraction for Channel 2"
    )
    channel_3_subtraction = param.ObjectSelector(
        default="N/A",
        objects=["N/A", "Channel 1", "Channel 2", "Channel 3", "Channel 4"],
        doc="Subtraction for Channel 3"
    )
    channel_4_subtraction = param.ObjectSelector(
        default="N/A",
        objects=["N/A", "Channel 1", "Channel 2", "Channel 3", "Channel 4"],
        doc="Subtraction for Channel 4"
    )

    channel_1_offset = param.Number(0.0, precedence=0)
    channel_2_offset = param.Number(0.0, precedence=0)
    channel_3_offset = param.Number(0.0, precedence=0)
    channel_4_offset = param.Number(0.0, precedence=0)
    
    buffer = param.ClassSelector(class_=SharedBuffer, precedence=-1)

    @param.depends(
            "channel_1_subtraction", 
            "channel_2_subtraction", 
            "channel_3_subtraction", 
            "channel_4_subtraction", 
            "channel_1_offset", 
            "channel_2_offset", 
            "channel_3_offset", 
            "channel_4_offset"
        )
    def sin_curves(self, data: pd.DataFrame):
        data = data.sort_values(by="timestamp").tail(300)
        # use the object selectors to subtract the selected channel from the other channels with an offset, lower() is used to convert the channel name to lowercase and replace the underscore with a space
        if self.channel_1_subtraction.lower() != "n/a":
            data["channel_1"] = data["channel_1"] - data[self.channel_1_subtraction.lower().replace(" ", "_")]
        if self.channel_2_subtraction.lower() != "n/a":
            data["channel_2"] = data["channel_2"] - data[self.channel_2_subtraction.lower().replace(" ", "_")]
        if self.channel_3_subtraction.lower() != "n/a":
            data["channel_3"] = data["channel_3"] - data[self.channel_3_subtraction.lower().replace(" ", "_")]
        if self.channel_4_subtraction.lower() != "n/a":
            data["channel_4"] = data["channel_4"] - data[self.channel_4_subtraction.lower().replace(" ", "_")]  
        data["channel_1"] = data["channel_1"] + self.channel_1_offset
        data["channel_2"] = data["channel_2"] + self.channel_2_offset
        data["channel_3"] = data["channel_3"] + self.channel_3_offset
        data["channel_4"] = data["channel_4"] + self.channel_4_offset

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
