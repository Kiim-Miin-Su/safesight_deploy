FROM python:3.9-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./app ./app
COPY ./static ./static
COPY ./weights/helmet_best.pt ./weights/helmet_best.pt
COPY ./weights/vest_best.pt ./weights/vest_best.pt
COPY ./weights/person_best.pt ./weights/person_best.pt
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
