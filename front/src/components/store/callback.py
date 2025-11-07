from ast import parse
from datetime import date
from validation.date import parse_and_check_datetime
from store.store import ERROR, PREDICTION_POINTS, check_store
from store.point import PREDICTION, TIMESTAMP
from api import BTCPrediction


def handle_datetime_input(store: dict, new_datetime_str: str) -> dict:
  if not check_store(store):
    return {
       PREDICTION_POINTS: [],
       ERROR: ''
    }

  # Check date, ironically, this will never be trigged because the datetime input does this for us :)
  parsed_datetime, date_error = parse_and_check_datetime(new_datetime_str)
  if parsed_datetime is None:
      print(new_datetime_str, date_error)
      store[ERROR] = date_error
      return store

  prediction = BTCPrediction.predict(parsed_datetime)

  # Request failed
  if prediction is None:
      store[ERROR] = "Error getting prediction"
      return store
  
  store[PREDICTION_POINTS].append({
     TIMESTAMP: parsed_datetime,
     PREDICTION: prediction
  })

  print("new store", store)

  return store