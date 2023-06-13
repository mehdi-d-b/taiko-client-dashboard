import param
import datetime.datetime
import requests
import holoviews as hv 
import pandas as pd, numpy as np
from holoviews.streams import Buffer
import panel as pn

from tornado.ioloop import PeriodicCallback
from tornado import gen

class Prover(param.Parameterized):

    mock_param = param.Number(0.0, precedence=0)

    df = pd.DataFrame({
        'timestamp': np.array([]),
        'proofs_generated': np.array([]),
        'proving_time': np.array([]),
        'earnings': np.array([]),
        'eth_left_l1': np.array([])})
    df.set_index('timestamp', inplace=True)

    buffer = Buffer(data=df, length=1000)
    
    @param.depends('mock_param')    
    def get_info(self,data):
        return ( 
            pn.indicators.Trend(title='Earnings', data=data[["timestamp","earnings"]]) +
            pn.indicators.Trend(title='Proofs Generated', data=data[["timestamp","proofs_generated"]]) +
            pn.indicators.Trend(title='ETH left on L1', data=data[["timestamp","eth_left_l1"]]) +
            pn.indicators.Number(name='Average proving time', value=data[["proving_time"]].mean(), format='{value}s')
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
            'proving_time': [data['']],
            'eth_left_l1': [data['']]})
        )
    
    def view(self):
        PeriodicCallback(self.get_data, 1000*10).start()
        return hv.DynamicMap(self.get_info ,streams=[self.buffer]).opts(
             width=1200, 
             height=600,
             title='Prover',
             tools=['hover']
        )