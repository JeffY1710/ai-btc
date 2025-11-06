from fastapi import FastAPI, status
import random

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/predict/{datetime}")
async def predict(datetime: str):
    return {"datetime": datetime, "prediction": random.random()}


class HealthCheck():
    status: str = "OK"


@app.get("/healthcheck/")
async def healthcheck():
    return {"status": "ok"}
