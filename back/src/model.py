import mlflow
import mlflow.sklearn as mlflow_sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd

datetime_column = 'Open time'
filename = 'https://raw.githubusercontent.com/JeffY1710/ai-btc/refs/heads/feature/data/data/binance_1d.csv'
# DATAFRAME = pd.read_csv('https://raw.githubusercontent.com/JeffY1710/ai-btc/refs/heads/feature/data/data/binance_1d.csv')

def read_file_sort_date(filename: str):
    df = pd.read_csv(filename)
    df = df.dropna()
    df[datetime_column] = pd.to_datetime(df[datetime_column])
    return df.sort_values(by=datetime_column, ascending=False)


def get_df_by_year(df, year):
    return df[df[datetime_column].dt.year == year]


def get_df_exclude_year(df, year):
    return df[df[datetime_column].dt.year != year]


def add_datetime_detail(df):
    df.loc[:, 'unixdate'] = pd.to_numeric(df[datetime_column])
    df.loc[:, 'day'] = df[datetime_column].dt.day
    df.loc[:, 'month'] = df[datetime_column].dt.month
    df.loc[:, 'year'] = df[datetime_column].dt.year


df = read_file_sort_date(filename)
df_2025 = get_df_by_year(df, 2025)
df_train = get_df_exclude_year(df, 2025)

add_datetime_detail(df)
add_datetime_detail(df_2025)
add_datetime_detail(df_train)

X_train = df_train[['Low', 'unixdate', 'Open', 'Close']]
y_train = df_train['High']

X_test = df_2025[['Low', 'unixdate', 'Open', 'Close']]
y_test = df_2025['High']

rf = RandomForestRegressor(n_estimators=100, random_state=0, max_features=1)

# Démarre une expérience MLflow
mlflow.set_experiment("binance_randomforest")

with mlflow.start_run():
    rf.fit(X_train, y_train)

    p_2025 = rf.predict(X_test)
    r2 = r2_score(y_test, p_2025)
    mse = mean_squared_error(y_test, p_2025)
    rmse = np.sqrt(mse)

    # Log des métriques
    mlflow.log_metric("r2_score", r2)
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("rmse", rmse)

    # Log des paramètres
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_features", 1)

    # Sauvegarde du modèle
    mlflow_sklearn.log_model(rf, "model")
