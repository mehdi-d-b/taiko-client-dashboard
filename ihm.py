import requests
import asyncio

import panel as pn, holoviews as hv 
from panel.widgets import FloatInput

from utils.sensor import SharedBuffer, Sensor

pn.config.sizing_mode = 'stretch_width'
hv.extension('bokeh', logo=False)

# We will share the buffer instance among all users/ sessions
# to avoid having lots of instances all reading data from the redis cache
shared_buffer = pn.state.as_cached("shared_buffer", SharedBuffer)
sensor = Sensor(buffer=shared_buffer)
    
hv.renderer('bokeh').theme = 'caliber'

pn.template.FastListTemplate(
    site="Panel", 
    title="Real-time IoT Dashboard", 
    sidebar=["Use the widgets to change the data."], 
    main=[
        pn.Tabs(
            ('Sensor data', 
             pn.Column(
                pn.Row(sensor.view),
                pn.Row(
                        pn.Column(sensor.param.channel_1_subtraction, sensor.param.channel_1_offset),
                        pn.Column(sensor.param.channel_2_subtraction, sensor.param.channel_2_offset),
                        pn.Column(sensor.param.channel_3_subtraction, sensor.param.channel_3_offset),
                        pn.Column(sensor.param.channel_4_subtraction, sensor.param.channel_4_offset)
                )
            )
            )
        )
    ]
).servable();