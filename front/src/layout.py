from dash import html

from components.table import table
from components.timeframe_selector import timeframe_selector
from components.graph import graph
from components.store.component import store
from components.input import input
from components.output import output

def add_layout(app):
  app.layout = html.Div([
    table(),

    html.Hr(),
    
    timeframe_selector(),
    graph(app),
    
    html.Hr(),
    
    input(app),
    output(app),

    store()
  ])