from datetime import date, datetime
from dash import html, dcc, Input, Output, State
from validation.date import ALLOWED_TIMESTAMP_IN_YEARS
from components.store.callback import handle_datetime_input

def input(app):
  @app.callback(
    Output('prediction-store', 'data'),
    Input('predict-button', 'n_clicks'),
    State('datetime-input', 'date'),
    State('prediction-store', 'data')
  )
  def store_prediction(predict_button_clicks: int, datetime_input: str, store: dict):
    if not predict_button_clicks or not datetime_input:
        return store

    return handle_datetime_input(store, datetime_input) 

  now = datetime.now()

  return html.Div([
    html.Label("Select datetime for prediction:"),

    dcc.DatePickerSingle(
        id='datetime-input',
        min_date_allowed=date(now.year, now.month, now.day+1),
        max_date_allowed=date(now.year + ALLOWED_TIMESTAMP_IN_YEARS, now.month, now.day),
        date=date(now.year, now.month, now.day)
    ),
    
    html.Button('Predict', id='predict-button', n_clicks=0)
  ])