from datetime import timedelta, datetime
from enum import Enum

from pandas import DataFrame, to_datetime
from dash import html, dcc

class Timeframe(Enum):
  DAY = 'D'
  WEEK = 'W'
  MONTH = 'M'
  YEAR = 'Y'
  FULL = 'F'

def timeframe_selector():
  return html.Div([
    html.Label("Select Timeframe:"),

    dcc.Dropdown(
        id='timeframe-dropdown',
        options=[
            {'label': 'Day', 'value': Timeframe.DAY.value},
            {'label': 'Week', 'value': Timeframe.WEEK.value},
            {'label': 'Month', 'value': Timeframe.MONTH.value},
            {'label': 'Year', 'value': Timeframe.YEAR.value},
            {'label': 'Full', 'value': Timeframe.FULL.value}
        ],
        value=Timeframe.WEEK.value
    )
  ])

def filter_dataframe_by_timeframe(df: DataFrame, timeframe_value: str, time_column_name: str):
    now = datetime.now()

    if timeframe_value == Timeframe.DAY.value:
        start = now - timedelta(days=1)
    elif timeframe_value == Timeframe.WEEK.value:
        start = now - timedelta(weeks=1)
    elif timeframe_value == Timeframe.MONTH.value:
        start = now - timedelta(days=30)
    elif timeframe_value == Timeframe.YEAR.value:
        start = now - timedelta(days=365)
    elif timeframe_value == Timeframe.FULL.value:
        return df
    
    df[time_column_name] = to_datetime(df[time_column_name])

    return df[df[time_column_name] >= start]