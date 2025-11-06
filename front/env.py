from dotenv import load_dotenv
import os

def read_env(variable, default=None):
    data = os.getenv(variable, default)
    if data is None or len(data) == 0:
        raise RuntimeError(f"Missing required environment variable: {variable}")
    return data

load_dotenv() # Load .env

BACKEND_URL = read_env("BACKEND_URL")
DATASET_URL = read_env("DATASET_URL")
PORT = int(read_env("PORT", "8050"))
