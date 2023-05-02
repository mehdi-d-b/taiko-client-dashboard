import param
import math
import random
import time

import holoviews as hv 
import pandas as pd, numpy as np
from holoviews.streams import Buffer

from tornado.ioloop import PeriodicCallback
from tornado import gen
import panel as pn

INITIAL_DATA = pd.DataFrame(
    {
        "timestamp": np.array([]),
        "channel_1": np.array([]),
        "channel_2": np.array([]),
        "channel_3": np.array([]),
        "channel_4": np.array([]),
    }
)
INITIAL_DATA.set_index("timestamp", inplace=True)


class SharedBuffer(param.Parameterized):
    value = param.ClassSelector(class_=Buffer)
    last_update = param.Date()

    def __init__(self, **params):
        params.update(
            value = Buffer(data=INITIAL_DATA, length=5000),
            last_update = pd.Timestamp.now(),
        )
        super().__init__(**params)
                
        PeriodicCallback(self.sin_data, 100).start()

    @gen.coroutine
    def sin_data(self):
        timestamp = int(time.time() * 1000)
        data = pd.DataFrame({
                'timestamp': [timestamp],
                'channel_1': [generate_data(0, timestamp)],
                'channel_2': [generate_data(1, timestamp)],
                'channel_3': [generate_data(2, timestamp)],
                'channel_4': [generate_data(3, timestamp)]})
        self.value.send(data)


class Frequencemetre(param.Parameterized):
    
    # Channel 1 params
    channel_1_subtract = param.ObjectSelector(
        default="N/A",
        objects=["N/A", "Channel 2", "Channel 3", "Channel 4"],
        doc="Channel 1 subtraction"
    )
    channel_1_offset = param.Number(0.0, precedence=0)
    
    # Channel 2 params
    channel_2_subtract = param.ObjectSelector(
        default="N/A",
        objects=["N/A", "Channel 1", "Channel 3", "Channel 4"],
        doc="Channel 2 subtraction"
    )
    channel_2_offset = param.Number(0.0, precedence=0)
    
    # Channel 3 params
    channel_3_subtract = param.ObjectSelector(
        default="N/A",
        objects=["N/A", "Channel 1", "Channel 2", "Channel 4"],
        doc="Channel 1 subtraction"
    )
    channel_3_offset = param.Number(0.0, precedence=0)
    
    # Channel 4 params
    channel_4_subtract = param.ObjectSelector(
        default="N/A",
        objects=["N/A", "Channel 1", "Channel 2", "Channel 3"],
        doc="Channel 4 subtraction"
    )
    channel_4_offset = param.Number(0.0, precedence=0)

    
    
    buffer = param.ClassSelector(class_=SharedBuffer, precedence=-1)

    @param.depends("channel_1_subtract",
                   "channel_1_offset",
                   "channel_2_subtract",
                   "channel_2_offset",
                   "channel_3_subtract",
                   "channel_3_offset",
                   "channel_4_subtract",
                   "channel_4_offset",
                   )
    def sin_curves(self, data: pd.DataFrame):
        data = data.sort_values(by="timestamp").tail(500)
        
        # Channel 1
        if self.channel_1_subtract != "N/A":
            data["channel_1"] -= data["channel_" + str(self.channel_1_subtract)[-1]]
        data["channel_1"] += self.channel_1_offset
        # Channel 2
        if self.channel_2_subtract != "N/A":
            data["channel_2"] -= data["channel_" + str(self.channel_2_subtract)[-1]]
        data["channel_2"] += self.channel_2_offset
        # Channel 3
        if self.channel_3_subtract != "N/A":
            data["channel_3"] -= data["channel_" + str(self.channel_3_subtract)[-1]]
        data["channel_3"] += self.channel_3_offset
        # Channel 4
        if self.channel_4_subtract != "N/A":
            data["channel_4"] -= data["channel_" + str(self.channel_1_subtract)[-1]]
        data["channel_4"] += self.channel_4_offset
        
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
            title="Real-time device data", 
            tools=["hover"], 
            legend_position='top_left'
        )

def generate_data(channel_num, timestamp):
    """
    This function create sinusoides depending on the channel number of the
    device.

    Parameters
    ----------
    channel_num : INT
        Channel number.
    timestamp : INT
        Current timestamp.

    Returns
    -------
    sine_val : FLOAT
        Sine's value.

    """
    sine_val = float(pn.state.cache['amplitude']) * math.sin(float(pn.state.cache['freq'] + channel_num/5.0) *   timestamp / 1000.0) + channel_num
    
    sine_val += random.uniform(
        -pn.state.cache['noise_amplitude'], 
        pn.state.cache['noise_amplitude'])
    return sine_val
    