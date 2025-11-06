# AI-BTC Frontend

## What
Used so the client can see the BTC price prediction.

## Stack
Built with `Dash`.

## Running the frontend
```bash
cd front
docker build -t dash-front .
docker run -p 80:8050 dash-front
```