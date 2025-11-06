from pathlib import Path
from dotenv import load_dotenv
import os

# Helper to check if env variable is set
def read_env(variable, default=None):
    data = os.getenv(variable, default)
    if data is None or len(data) == 0:
        raise RuntimeError(f"Missing required environment variable: {variable}")
    return data

# Get env path
env_path = Path.joinpath(Path(__file__).resolve().parent.parent, ".env")
if not env_path.exists():
    print(f"Warning: .env file not found at {env_path}")

# Load env
load_dotenv(env_path)

BACKEND_URL = read_env("BACKEND_URL")
DATASET_URL = read_env("DATASET_URL")
PORT = int(read_env("PORT", "8050"))
