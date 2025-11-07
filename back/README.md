# AI-BTC Backend

## What
Bridge between Web client and MlFlow model

## Stack
Built with `FastAPI`.

# Availaible routes

`GET /healthcheck`
```json
{
  "status": "ok",
  "model_loaded": true,
  "data_loaded": true,
  "shap_initialized": true,
  "shap_info": {
      "base_value": 36838.699251867365,
      "feature_importance": {
          "Low": 20751.49396239202,
          "Open": 24960.537675425356,
          "Close": 22037.066526528724,
          "day": 42.352816527876485,
          "month": 406.1478139508682,
          "year": 9572.632362212638
      },
      "most_important_feature": "Open"
  }
}
```

___

`POST /predict`

Input
```json
{
    "datetime": "2026-11-03",
    "low": 10500,
    "open": 101500,
    "close": 106431
}
```

Output
```json
{
    "datetime": "2026-11-03",
    "prediction": 79319.14830000002,
    "input_features": {
        "low": 10500.0,
        "open": 101500.0,
        "close": 106431.0,
        "day": 3,
        "month": 11,
        "year": 2026
    }
}
```

____

`POST /predict/future`

Input
```json
{
    "target_date": "2025-11-06"
}
```

Output
```json
{
  "datetime": "2025-11-06",
  "prediction": 107157.29255000014,
  "input_features": {
      "low": 105852.37,
      "open": 106583.05,
      "close": 106590.18,
      "day": 6,
      "month": 11,
      "year": 2025,
      "based_on_date": "2025-11-04"
  }
}
```

# Running the backend
```bash
cd back
docker build -t ai-btc-back .
docker run -p 8000:8000 ai-btc-back
```