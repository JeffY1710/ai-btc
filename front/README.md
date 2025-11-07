# AI-BTC Frontend

## What
Used so the client can see the BTC price prediction.

## Features
- Shows graph of current BTC prices
- Predict an amount at date
- Shows a detailled table of the current dataset

## Stack
Built with `Dash`.

## Running the frontend
```bash
cd front
docker build -t ai-btc-front .
docker run -p 80:8050 ai-btc-front
```