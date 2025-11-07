from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow
import mlflow.sklearn
import pandas as pd
from datetime import datetime, timedelta
import shap
import numpy as np

app = FastAPI()

MODEL_URI = None
MODEL = None
MODEL_NAME = 'binance_randomforest_date_features'
DATAFRAME = None
SHAP_EXPLAINER = None
SHAP_BASE_VALUE = None
SHAP_FEATURE_IMPORTANCE = None
BINANCE_DATA_URL = 'https://raw.githubusercontent.com/JeffY1710/ai-btc/refs/heads/feature/data/data/binance_1d.csv'


def load_historical_data():
    """Charge les données historiques Binance"""
    global DATAFRAME
    try:
        df = pd.read_csv(BINANCE_DATA_URL)
        df['Open time'] = pd.to_datetime(df['Open time'], utc=True)
        df['Open time'] = df['Open time'].dt.tz_localize(None)   
        df = df.sort_values(by='Open time', ascending=False)
        DATAFRAME = df
        print(f"Données chargées: {len(df)} lignes (jusqu'à {df['Open time'].iloc[0].date()})")
    except Exception as e:
        print(f"Erreur lors du chargement des données: {e}")


def load_model():
    """Charge le dernier modèle depuis MLflow"""
    global MODEL, MODEL_URI
    try:
        client = mlflow.tracking.MlflowClient()

        experiment = client.get_experiment_by_name(MODEL_NAME)
        if not experiment:
            print(f"Expérience '{MODEL_NAME}' non trouvée")
            return

        runs = client.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=["start_time DESC"],
            max_results=1
        )

        if runs:
            run_id = runs[0].info.run_id
            MODEL_URI = f"runs:/{run_id}/model"
            MODEL = mlflow.sklearn.load_model(MODEL_URI)
            print(f"Modèle chargé depuis le run: {run_id}")
        else:
            print("Aucun run trouvé pour cette expérience")
    except Exception as e:
        print(f"Erreur lors du chargement du modèle: {e}")


def initialize_shap():
    """Initialize SHAP explainer with sample data"""
    global SHAP_EXPLAINER, SHAP_BASE_VALUE, SHAP_FEATURE_IMPORTANCE
    
    if MODEL is None or DATAFRAME is None:
        print("Cannot initialize SHAP: model or data not loaded")
        return
    
    try:
        df_sample = DATAFRAME.head(100).copy()
        df_sample['day'] = pd.to_datetime(df_sample['Open time']).dt.day
        df_sample['month'] = pd.to_datetime(df_sample['Open time']).dt.month
        df_sample['year'] = pd.to_datetime(df_sample['Open time']).dt.year
        
        X_sample = df_sample[['Low', 'Open', 'Close', 'day', 'month', 'year']]
        
        SHAP_EXPLAINER = shap.TreeExplainer(MODEL)
        shap_values = SHAP_EXPLAINER.shap_values(X_sample)
        
        SHAP_BASE_VALUE = float(SHAP_EXPLAINER.expected_value)
        
        mean_abs_shap = np.abs(shap_values).mean(axis=0)
        SHAP_FEATURE_IMPORTANCE = {
            feature: float(importance) 
            for feature, importance in zip(X_sample.columns, mean_abs_shap)
        }
        
        print(f"SHAP initialized - Base value: {SHAP_BASE_VALUE:.2f}")
        
    except Exception as e:
        print(f"Erreur lors de l'initialisation SHAP: {e}")


@app.on_event("startup")
async def startup_event():
    load_historical_data()
    load_model()
    initialize_shap()


class PredictionInput(BaseModel):
    low: float
    open: float
    close: float
    datetime: str


class FuturePredictionInput(BaseModel):
    target_date: str


class PredictionOutput(BaseModel):
    datetime: str
    prediction: float
    input_features: dict

@app.get("/")
async def read_root():
    return {
        "message": "Binance High Price Predictor API",
        "model_loaded": MODEL is not None,
        "data_loaded": DATAFRAME is not None,
        "shap_initialized": SHAP_EXPLAINER is not None,
        "latest_data_date": str(DATAFRAME['Open time'].iloc[0]) if DATAFRAME is not None else None
    }


@app.post("/predict/", response_model=PredictionOutput)
async def predict(data: PredictionInput):
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")

    try:
        dt = pd.to_datetime(data.datetime)
        day = dt.day
        month = dt.month
        year = dt.year

        features = pd.DataFrame({
            'Low': [data.low],
            'Open': [data.open],
            'Close': [data.close],
            'day': [day],
            'month': [month],
            'year': [year]
        })

        pred = MODEL.predict(features)[0]

        return {
            "datetime": data.datetime,
            "prediction": float(pred),
            "input_features": {
                "low": data.low,
                "open": data.open,
                "close": data.close,
                "day": day,
                "month": month,
                "year": year
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")


@app.post("/predict/future/", response_model=PredictionOutput)
async def predict_future(data: FuturePredictionInput):
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")

    if DATAFRAME is None or DATAFRAME.empty:
        raise HTTPException(status_code=503, detail="Données historiques non chargées")

    try:
        target_date = pd.to_datetime(data.target_date).tz_localize(None)
        last_row = DATAFRAME.iloc[0]
        last_date = DATAFRAME['Open time'].iloc[0]
        max_future_date = last_date + timedelta(days=365)

        if target_date <= last_date:
            raise HTTPException(status_code=400, detail=f"La date doit être future (dernière date connue: {last_date.date()})")
        if target_date > max_future_date:
            raise HTTPException(status_code=400, detail=f"La date ne peut pas dépasser +1 an ({max_future_date.date()})")

        low = float(last_row['Low'])
        open_price = float(last_row['Open'])
        close = float(last_row['Close'])

        day = target_date.day
        month = target_date.month
        year = target_date.year

        features = pd.DataFrame({
            'Low': [low],
            'Open': [open_price],
            'Close': [close],
            'day': [day],
            'month': [month],
            'year': [year]
        })

        pred = MODEL.predict(features)[0]

        return {
            "datetime": data.target_date,
            "prediction": float(pred),
            "input_features": {
                "low": low,
                "open": open_price,
                "close": close,
                "day": day,
                "month": month,
                "year": year,
                "based_on_date": str(last_date.date())
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")


@app.get("/predict/future/{date_str}")
async def predict_future_simple(date_str: str):
    return await predict_future(FuturePredictionInput(target_date=date_str))


@app.get("/healthcheck/")
async def healthcheck():
    health_info = {
        "status": "ok",
        "model_loaded": MODEL is not None,
        "data_loaded": DATAFRAME is not None,
        "shap_initialized": SHAP_EXPLAINER is not None
    }
    
    # Add SHAP info if available
    if SHAP_EXPLAINER is not None:
        health_info["shap_info"] = {
            "base_value": SHAP_BASE_VALUE,
            "feature_importance": SHAP_FEATURE_IMPORTANCE,
            "most_important_feature": max(SHAP_FEATURE_IMPORTANCE, key=SHAP_FEATURE_IMPORTANCE.get) if SHAP_FEATURE_IMPORTANCE else None
        }
    
    return health_info