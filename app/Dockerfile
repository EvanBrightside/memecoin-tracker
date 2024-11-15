# app/Dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/models

COPY . .

CMD ["sh", "-c", "python scripts/init_db.py && python scripts/train_model.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
