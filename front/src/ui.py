from dash import Dash, html, dash_table

from data import DATAFRAME

def user_interface(PORT: int):
  app = Dash(__name__)
  app.layout = [
        html.Div(children='BTC Prediction'),
        dash_table.DataTable(data=DATAFRAME.to_dict('records'), page_size=10)
    ]
  app.run(port=PORT)