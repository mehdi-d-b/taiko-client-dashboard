import panel as pn, holoviews as hv 

from utils.node import Node
from utils.prover import Prover
from utils.proposer import Proposer

pn.config.sizing_mode = 'stretch_width'
hv.extension('bokeh', logo=False)
hv.renderer('bokeh').theme = 'caliber'

node = Node()
prover = Prover()
proposer = Proposer()

prover_indicator = pn.indicators.BooleanStatus(width=10, height=10, value=True, color='success')
proposer_indicator = pn.indicators.BooleanStatus(width=10, height=10, value=True, color='warning')
prover_status = pn.Column('Prover', prover_indicator, 'Online')
proposer_status = pn.Column('Proposer', proposer_indicator, 'Sync')


pn.template.FastListTemplate(
    site="Panel", 
    title="Taiko Client Dashboard", 
    logo='doc/taiko-icon-mono.png',
    favicon='doc/taiko-icon-wht.png',
    accent_base_color='#ff00ff',
    header_neutral_color='#ff00ff',
    header_background ='#ff00ff',
    header_accent_base_color ='#ff00ff',
    sidebar=[],
    collapsed_sidebar=True, 
    main=[
        pn.Row('Prover', prover_indicator, 'Online', 'Proposer', proposer_indicator, 'Sync'),
        pn.Tabs(
            ('Node', node.view),
            ('Prover', prover.view),
            ('Proposer', proposer.view),
        )
    ]
).servable();
