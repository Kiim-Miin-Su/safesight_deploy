FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY safesight_api/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
