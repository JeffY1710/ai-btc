from dash import html, Output, Input
from store.store import ERROR

def output(app):
  @app.callback(
    Output('prediction-output', 'children'),
    Input('prediction-store', 'data')
  )
  def update_prediction_output(store: dict):
    if not store:
      return ''

    return store[ERROR] if len(store[ERROR]) > 0 else ''

  return html.Div(id='prediction-output')
