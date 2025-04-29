FROM python:3.9-slim-bullseye

WORKDIR /app

# OpenCV 필요한 최소 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 코드 복사
COPY ./app ./app
COPY ./weights ./weights
COPY ./static ./static
COPY ./templates ./templates
COPY requirements.txt .

# pip install
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --find-links https://download.pytorch.org/whl/cpu/ -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
