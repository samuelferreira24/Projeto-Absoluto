FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends docker.io ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "mcp>=1.9,<2" "docker>=7,<8" "uvicorn>=0.30,<1"

WORKDIR /app
COPY main.py /app/main.py

EXPOSE 8788
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8788"]
