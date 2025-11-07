FROM python:3.14-slim

WORKDIR /app

RUN pip install uv

COPY .env pyproject.toml uv.lock ./

RUN ["uv", "sync"]

COPY src ./src

# Default Dash port
EXPOSE 8050

CMD ["uv", "run", "python", "src/main.py"]
