FROM python:3.9-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./app ./app
COPY ./static ./static
COPY ./templates ./templates
COPY ./weights ./weights
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "pip install ultralytics && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
