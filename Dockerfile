FROM python:3.9-slim-bullseye

WORKDIR /app

# 시스템 기본 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 코드 복사
COPY ./app ./app
COPY ./weights ./weights
COPY ./templates ./templates
COPY ./static ./static
COPY requirements.txt .

# 필요한 파이썬 패키지 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --find-links https://download.pytorch.org/whl/cpu/ -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
