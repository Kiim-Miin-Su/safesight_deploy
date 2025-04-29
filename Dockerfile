FROM python:3.9-slim

WORKDIR /app

COPY ./app /app/app
COPY ./static /app/static
COPY requirements.txt /app/requirements.txt

# torch, torchvision은 경량 버전으로
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
