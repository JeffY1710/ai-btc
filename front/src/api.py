from datetime import datetime
import requests
from env import BACKEND_URL
from utils import response_handler


class BTCPrediction():
  def predict(date: datetime) -> float | None:
    date_string = date.strftime("%Y-%m-%d")
    url = f"{BACKEND_URL}/predict/future"

    payload = {
      "target_date": date_string
    }

    ok, data = response_handler("post", url, json=payload)
    if not ok:
       return None

    prediction = float(data['prediction'])
    return prediction

  def health_check() -> bool:
    url = f"{BACKEND_URL}/healthcheck"

    ok, data = response_handler("get", url)
    if not ok:
       return False

    is_status_ok = data['status'] == "ok"
    return is_status_ok