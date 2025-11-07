import mlflow
import mlflow.sklearn as mlflow_sklearn
from mlflow.models.signature import infer_signature
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
from datetime import datetime

datetime_column = 'Open time'
filename = 'https://raw.githubusercontent.com/JeffY1710/ai-btc/refs/heads/feature/data/data/binance_1d.csv'
shapes_info = None

def read_file_sort_date(filename: str):
    df = pd.read_csv(filename)
    df = df.dropna()
    df[datetime_column] = pd.to_datetime(df[datetime_column])
    return df.sort_values(by=datetime_column, ascending=True)

def add_datetime_detail(df):
    df = df.copy()
    df['day'] = df[datetime_column].dt.day
    df['month'] = df[datetime_column].dt.month
    df['year'] = df[datetime_column].dt.year
    return df

df = read_file_sort_date(filename)
df = add_datetime_detail(df)

print(f"✅ Données chargées : {len(df)} lignes jusqu'au {df[datetime_column].max().date()}")

X = df[['Low', 'Open', 'Close', 'day', 'month', 'year']]
y = df['High']

rf = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    max_features='sqrt',
    n_jobs=-1
)

mlflow.set_experiment("binance_randomforest_date_features")

with mlflow.start_run():
    rf.fit(X, y)
    
    signature = infer_signature(X, rf.predict(X))
    
    mlflow.log_param("n_estimators", 200)
    mlflow.log_param("max_features", "sqrt")
    mlflow.log_param("training_rows", len(df))
    
    mlflow_sklearn.log_model(
        sk_model=rf,
        name="model",
        signature=signature,
        input_example=X.head(1)
    )

    
    
    print(f"Modèle entraîné et enregistré dans MLflow Run ID: {mlflow.active_run().info.run_id}")

def predict_future_date(model, last_row, target_date_str):
    target_date = pd.to_datetime(target_date_str)
    day = target_date.day
    month = target_date.month
    year = target_date.year

    features = pd.DataFrame({
        'Low': [last_row['Low']],
        'Open': [last_row['Open']],
        'Close': [last_row['Close']],
        'day': [day],
        'month': [month],
        'year': [year]
    })
    
    pred = model.predict(features)[0]
    
    return {
        "target_date": target_date_str,
        "prediction": float(pred),
        "based_on_date": str(last_row[datetime_column].date())
    }