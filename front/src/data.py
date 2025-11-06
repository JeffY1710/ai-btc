import pandas as pd
from env import DATASET_URL

DATAFRAME = pd.read_csv(DATASET_URL)

DATAFRAME['Open time'] = pd.to_datetime(DATAFRAME['Open time'])
DATAFRAME['timestamp'] = pd.to_numeric(DATAFRAME['Open time'])

DATAFRAME = DATAFRAME.sort_values(by='Open time')

if not {'Open time', 'Close'}.issubset(DATAFRAME.columns):
  raise RuntimeError("Dataset doesn't have 'Open time' or/and 'Close'")