from pandas import DataFrame
from dash import dcc, Output, Input
import plotly.graph_objects as go
from components.timeframe_selector import filter_dataframe_by_timeframe
from data import DATAFRAME
from store.store import PREDICTION_POINTS, check_store

def draw_dataframe(fig: go.Figure, df: DataFrame):
  fig.add_trace(go.Scatter(
      x=df['Open time'],
      y=df['High'],
      mode='lines',
      name='Historical BTC Price'
  ))

def draw_prediction(fig: go.Figure, df_predictions: DataFrame):
  fig.add_trace(go.Scatter(
    x=df_predictions['timestamp'],
    y=df_predictions['prediction'],
    mode='markers',
    name='Predicted Points',
    marker=dict(color='red', size=8, symbol='circle')
  ))

def graph_layout(fig: go.Figure):
  fig.update_layout(
      title='Bitcoin Price Prediction',
      xaxis_title='Timestamp',
      yaxis_title='Price'
  )

def graph(app):
  @app.callback(
    Output('btc-graph', 'figure'),
    Input('timeframe-dropdown', 'value'),
    Input('prediction-store', 'data')
  )
  def update_graph_with_prediction(timeframe_value: str, store: dict):
    fig = go.Figure()

    df_filtered = filter_dataframe_by_timeframe(DATAFRAME, timeframe_value, 'Open time')

    draw_dataframe(fig, df_filtered)

    graph_layout(fig)

    if (not store) or (not check_store(store)) or (len(store.get(PREDICTION_POINTS, [])) == 0):
      return fig

    df_prediction = DataFrame(store[PREDICTION_POINTS])

    df_predictions_filtered = filter_dataframe_by_timeframe(df_prediction, timeframe_value, 'timestamp')

    draw_prediction(fig, df_predictions_filtered)

    graph_layout(fig)


    return fig 

  return dcc.Graph(id='btc-graph')