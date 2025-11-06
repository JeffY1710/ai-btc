import datetime
import requests
from env import BACKEND_URL
from utils import response_handler


class BTCPrediction():
  def predict(date: datetime) -> float | None:
    date_string = str(date)
    response = requests.get(f"{BACKEND_URL}/predict/{date_string}")
    ok, data = response_handler(response)
    if not ok:
       return None

    prediction = float(data['prediction'])
    return prediction

  def health_check() -> bool:
    response = requests.get(f"{BACKEND_URL}/healthcheck")
    ok, data = response_handler(response)
    if not ok:
       return False

    is_status_ok = data['status'] == "ok"
    return is_status_ok