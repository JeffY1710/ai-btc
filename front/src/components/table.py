from dash import dash_table
from data import DATAFRAME

def table():
  return dash_table.DataTable(
    data=DATAFRAME.to_dict('records'),
    page_size=10
  )