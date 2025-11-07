PREDICTION_POINTS = 'prediction_points'
ERROR = 'error'

def check_store(store: dict):
   return store and (PREDICTION_POINTS in store) and (ERROR in store) and (type(store[PREDICTION_POINTS]) == list)