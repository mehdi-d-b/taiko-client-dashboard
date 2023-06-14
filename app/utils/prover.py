import param
from datetime import datetime
import requests
import holoviews as hv 
import pandas as pd, numpy as np
from holoviews.streams import Buffer
import random

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
    #df.set_index('timestamp', inplace=True)

    buffer = Buffer(data=df, length=1000)
    
    @param.depends('mock_param')    
    def get_info(self,data):
        return hv.Layout( 
            hv.Area(label='Earnings', data=data[["timestamp","earnings"]]).opts(height=400, responsive=True, title="Earnings", labelled=[]) +
            hv.Area(label='Proofs Generated', data=data[["timestamp","proofs_generated"]]).opts(height=400, responsive=True, title="Proofs Generated", labelled=[]) +
            hv.Area(label='ETH left on L1', data=data[["timestamp","eth_left_l1"]]).opts(height=400, responsive=True, title="ETH left on L1", labelled=[]) +
            hv.Area(label='Average proving time', data=data[["timestamp","proving_time"]]).opts(height=400, responsive=True, title="Average proving time", labelled=[])
        ).cols(2)

    @gen.coroutine
    def get_data(self):
        r = requests.get('http://host.docker.internal:6060/debug/metrics') 
        # Parse data to json
        data = r.json()
        # Get the tags
        self.buffer.send(pd.DataFrame({
            'timestamp': [datetime.now()],
            'proofs_generated': [data['']],
            'proving_time': [data['']],
            'earnings': [data['']],
            'eth_left_l1': [data['']]})
        )


    @gen.coroutine
    def get_random_data(self):
        # Get the tags
        self.buffer.send(pd.DataFrame({
            'timestamp': [datetime.now()],
            'proofs_generated': [random.randint(1, 10)],
            'proving_time': [random.randint(1, 10)],
            'earnings': [random.randint(1, 10)],
            'eth_left_l1': [random.randint(1, 10)]})
        )
    
    def view(self):
        PeriodicCallback(self.get_random_data, 1000*1).start()
        return hv.DynamicMap(self.get_info ,streams=[self.buffer]).opts(
             title='Prover'
        )