import requests
import asyncio

import panel as pn, holoviews as hv 
from panel.widgets import FloatInput

from utils.frequencemetre import SharedBuffer, Frequencemetre

pn.config.sizing_mode = 'stretch_width'
hv.extension('bokeh', logo=False)

pn.extension(notifications=True)

# We will share the buffer instance among all users/ sessions
# to avoid having lots of instances all reading data from the redis cache
shared_buffer = pn.state.as_cached("shared_buffer", SharedBuffer)


# POST requests params
URL = 'http://localhost:5000/set_sine_params'
HEADERS = {'Content-type': 'application/json'}

# We will share the buffer instance among all users/ sessions
# to avoid having lots of instances all reading data from the redis cache
shared_buffer = pn.state.as_cached("shared_buffer", SharedBuffer)
frequencemetre = Frequencemetre(buffer=shared_buffer)

# Declare widgets
async def change_sin_amp(event):
    data = {'amplitude': event.new}
    requests.post(URL, json=data, headers=HEADERS)
    pn.state.notifications.success('Amplitude changée (succès)!', duration=2500)

async def change_sin_freq(event):
    data = {'freq': event.new}
    requests.post(URL, json=data, headers=HEADERS) 
    pn.state.notifications.success('Fréquence changée! (info)', duration=2500)

async def change_sin_noise(event):
    data = {'noise_amplitude': event.new}
    requests.post(URL, json=data, headers=HEADERS)
    pn.state.notifications.success('Bruit changé! (warning)', duration=2500)

sin_amp = FloatInput(name="Sine amplitude:", start=0.1, end=10, value=1, step = 0.1)
sin_amp.param.watch(change_sin_amp, 'value')

sin_freq = FloatInput(name="Sine frequency:", start=0.001, end=10, value=1, step = 0.1)
sin_freq.param.watch(change_sin_freq, 'value')

sin_noise = FloatInput(name="Sine noise:", start=0, end=10, value=0, step = 0.1)
sin_noise.param.watch(change_sin_noise, 'value')
    
hv.renderer('bokeh').theme = 'caliber'
controls = pn.WidgetBox('# Commandes',
                        sin_amp,
                        sin_freq,
                        sin_noise,
                        )


pn.template.FastListTemplate(
    site="Panel", 
    title="CAID", 
    sidebar=[*controls], 
    main=[
        pn.Tabs(
            ('Sines', pn.Row(frequencemetre.view,pn.Column(frequencemetre.param, width=100))),
        ),
        #enum.view
    ]
).servable();