import param
from datetime import datetime
import requests
import holoviews as hv 
import pandas as pd, numpy as np
from holoviews.streams import Buffer
import random
from holoviews import opts

from tornado.ioloop import PeriodicCallback
from tornado import gen

class Node(param.Parameterized):

    mock_param = param.Number(0.0, precedence=0)

    df = pd.DataFrame({
            'timestamp': np.array([]),
            'system': np.array([]),
            'iowait': np.array([]),
            'geth': np.array([]),
            'alloc': np.array([]),
            'used': np.array([]),
            'held': np.array([]),
            'read': np.array([]),
            'write': np.array([]),
            'ingress': np.array([]),
            'egress': np.array([]),
            'peers': np.array([]),
            'dials': np.array([]),
            'serves': np.array([])})
    #df.set_index('timestamp', inplace=True)

    buffer = Buffer(data=df, length=120)

    @param.depends('mock_param')
    def get_curves(self,data):
        return hv.Layout( 
            (
                hv.Curve(data[["timestamp","system"]], label='system') * 
                hv.Curve(data[["timestamp","iowait"]], label='iowait') *
                hv.Curve(data[["timestamp","geth"]], label='geth') 
            ).opts(title="💻 CPU", responsive=True, height=400,legend_position='top_left', labelled=[]).opts(opts.Curve(tools=['vline'],)) +
            (
                hv.Curve(data[["timestamp","alloc"]], label='alloc') *
                hv.Curve(data[["timestamp","used"]], label='used') *
                hv.Curve(data[["timestamp","held"]], label='held') 
            ).opts(title="💾 Memory", responsive=True, height=400,legend_position='top_left', labelled=[] ).opts(opts.Curve(tools=['vline'],)) +
            (
                hv.Area(data[["timestamp","read"]], label='read') *
                hv.Area(data[["timestamp","write"]], label='write') 
            ).opts(title="💽 Disk", responsive=True, height=400,legend_position='top_left', labelled=[]).opts(opts.Area(tools=['vline'],fill_alpha=0.5)) +
            (
                hv.Curve(data[["timestamp","ingress"]], label='ingress') * 
                hv.Curve(data[["timestamp","egress"]], label='egress') 
            ).opts(title="🚗 Traffic", responsive=True, height=400,legend_position='top_left', labelled=[]).opts(opts.Curve(tools=['vline'],)) +
            (
                hv.Curve(data[["timestamp","peers"]], label='peers') * 
                hv.Curve(data[["timestamp","dials"]], label='dials') *
                hv.Curve(data[["timestamp","serves"]], label='serves') 
            ).opts(title="🌍 Peers", responsive=True, height=400,legend_position='top_left', labelled=[]).opts(opts.Curve(tools=['vline'],)),
        ).cols(3)

    @gen.coroutine
    def get_data(self):
        r = requests.get('http://host.docker.internal:6060/debug/metrics') 
        # Parse data to json
        data = r.json()
        # Get the tags
        self.buffer.send(pd.DataFrame({
            'timestamp': [datetime.now()],
            'alloc': [data['system/memory/allocs.mean']],
            'used': [data['system/memory/used']],
            'held': [data['system/memory/held']],
            'system': [data["system/cpu/sysload"]],
            'iowait': [data["system/cpu/syswait"]],
            'geth': [data["system/disk/readbytes"]],
            'write': [data["system/disk/writebytes"]],
            'ingress': [data["p2p/ingress.count"]],
            'egress': [data["p2p/ingress.count"]],
            'peers': [data["p2p/peers"]],
            'dials': [data["p2p/dials.count"]],
            'serves': [data["p2p/serves.count"]]})
        )
    

    @gen.coroutine
    def get_random_data(self):
        # Get the tags
        self.buffer.send(pd.DataFrame({
            'timestamp': [datetime.now()],
            'system': [random.randint(1, 10)],
            'iowait': [random.randint(1, 10)],
            'geth': [random.randint(1, 10)],
            'alloc': [random.randint(1, 10)],
            'used': [random.randint(1, 10)],
            'held': [random.randint(1, 10)],
            'read': [random.randint(1, 10)],
            'write': [random.randint(1, 10)],
            'ingress': [random.randint(1, 10)],
            'egress': [random.randint(1, 10)],
            'peers': [random.randint(1, 10)],
            'dials': [random.randint(1, 10)],
            'serves': [random.randint(1, 10)]})
        )

    def view(self):
        PeriodicCallback(self.get_random_data, 1000*1).start()
        return hv.DynamicMap(self.get_curves ,streams=[self.buffer])