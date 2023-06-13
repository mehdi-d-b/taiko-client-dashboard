import param
from datetime import datetime
import requests
import holoviews as hv 
import pandas as pd, numpy as np
from holoviews.streams import Buffer
import panel as pn
import random

from tornado.ioloop import PeriodicCallback
from tornado import gen

class Proposer(param.Parameterized):

    mock_param = param.Number(0.0, precedence=0)

    df = pd.DataFrame({
        'timestamp': np.array([]),
        'blocks_proposed': np.array([]),
        'earnings': np.array([]),
        'eth_left_l1': np.array([])})
    #df.set_index('timestamp', inplace=True)

    buffer = Buffer(data=df, length=1000)
    
    @param.depends('mock_param')    
    def get_info(self,data):
        return ( 
                hv.Area(label='Earnings', data=data[["timestamp","earnings"]]) + 
                hv.Area(label='Blocks Proposed', data=data[["timestamp","blocks_proposed"]]) +
                hv.Area(label='ETH left on L1', data=data[["timestamp","eth_left_l1"]])
        )

    @gen.coroutine
    def get_data(self):
        r = requests.get('http://host.docker.internal:6060/debug/metrics') 
        # Parse data to json
        data = r.json()
        # Get the tags
        self.buffer.send(pd.DataFrame({
            'timestamp': [datetime.now()],
            'blocks_proposed': [data['']],
            'earnings': [data['']],
            'eth_left_l1': [data['']]})
        )

    @gen.coroutine
    def get_random_data(self):
        # Get the tags
        self.buffer.send(pd.DataFrame({
            'timestamp': [datetime.now()],
            'blocks_proposed': [random.randint(1, 10)],
            'earnings': [random.randint(1, 10)],
            'eth_left_l1': [random.randint(1, 10)]})
        )
    
    def view(self):
        PeriodicCallback(self.get_random_data, 1000*10).start()
        return hv.DynamicMap(self.get_info ,streams=[self.buffer]).opts(
             width=1200, 
             height=600,
             title='Proposer',
             #tools=['hover']
        )