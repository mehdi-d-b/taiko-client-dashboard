import panel as pn, holoviews as hv 

from utils.node import Node
from utils.prover import Prover
from utils.proposer import Proposer

pn.config.sizing_mode = 'stretch_width'
hv.extension('bokeh', logo=False)

node = Node()
prover = Prover()
proposer = Proposer()
    
hv.renderer('bokeh').theme = 'caliber'

pn.template.FastListTemplate(
    site="Panel", 
    title="Taiko Client Dashboard", 
    sidebar=["Node Status."], 
    main=[
        pn.Tabs(
            ('Node', 
             pn.Column(
                pn.Row(sensor.view),
                pn.Row(
                        pn.Column(sensor.param.channel_1_subtraction, sensor.param.channel_1_offset),
                        pn.Column(sensor.param.channel_2_subtraction, sensor.param.channel_2_offset),
                        pn.Column(sensor.param.channel_3_subtraction, sensor.param.channel_3_offset),
                        pn.Column(sensor.param.channel_4_subtraction, sensor.param.channel_4_offset)
                )
            )
            ),
            ('Prover', 
             pn.Column(
                pn.Row(sensor.view),
                pn.Row(
                        pn.Column(sensor.param.channel_1_subtraction, sensor.param.channel_1_offset),
                        pn.Column(sensor.param.channel_2_subtraction, sensor.param.channel_2_offset),
                        pn.Column(sensor.param.channel_3_subtraction, sensor.param.channel_3_offset),
                        pn.Column(sensor.param.channel_4_subtraction, sensor.param.channel_4_offset)
                )
            )
            ),
            ('Proposer', 
             pn.Column(
                pn.Row(sensor.view),
                pn.Row(
                        pn.Column(sensor.param.channel_1_subtraction, sensor.param.channel_1_offset),
                        pn.Column(sensor.param.channel_2_subtraction, sensor.param.channel_2_offset),
                        pn.Column(sensor.param.channel_3_subtraction, sensor.param.channel_3_offset),
                        pn.Column(sensor.param.channel_4_subtraction, sensor.param.channel_4_offset)
                )
            )
            ),
        )
    ]
).servable();