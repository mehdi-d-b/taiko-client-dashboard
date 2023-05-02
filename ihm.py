import panel as pn, holoviews as hv 
from panel.widgets import FloatInput

from utils.frequencemetre import SharedBuffer, Frequencemetre
from utils.spectrogram import Spectrogram

pn.config.sizing_mode = 'stretch_width'
hv.extension('bokeh')

pn.extension(notifications=True)

# We will share the buffer instance among all users/ sessions
# to avoid having lots of instances all reading data from the redis cache
shared_buffer = pn.state.as_cached("shared_buffer", SharedBuffer)
frequencemetre = Frequencemetre(buffer=shared_buffer)


spectrogram = Spectrogram()


# Declare widgets
def change_sin_amp(event):
    pn.state.cache['amplitude'] = event.new
    pn.state.notifications.info('Amplitude changed!', duration=2500)

def change_sin_freq(event):
    pn.state.cache['freq'] = event.new 
    pn.state.notifications.info('Frequency changed!', duration=2500)

def change_sin_noise(event):
    pn.state.cache['noise'] = event.new
    pn.state.notifications.info('Noise changed!', duration=2500)

sin_amp = FloatInput(name="Sine amplitude:", start=0.1, end=10, value=1, step = 0.1)
sin_amp.param.watch(change_sin_amp, 'value')

sin_freq = FloatInput(name="Sine frequency:", start=0.001, end=10, value=1, step = 0.1)
sin_freq.param.watch(change_sin_freq, 'value')

sin_noise = FloatInput(name="Sine noise:", start=0, end=10, value=0, step = 0.1)
sin_noise.param.watch(change_sin_noise, 'value')
    
hv.renderer('bokeh').theme = 'caliber'
controls = pn.WidgetBox('# Device Controls',
                        sin_amp,
                        sin_freq,
                        sin_noise,
                        )

pn.template.FastListTemplate(
    site="Panel", 
    title="Real-time data from device", 
    sidebar=[*controls], 
    main=[
        pn.Tabs(
            ('Signal', pn.Row(frequencemetre.view,pn.Column(frequencemetre.param, width=100))),
            ('Spectrogram', pn.Row(spectrogram.view,pn.Column(spectrogram.param, width=100)))
        )
    ]
).servable();