FROM python:3.9-slim-bullseye

WORKDIR /app

# 필수 시스템 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 애플리케이션 코드 복사
COPY ./app ./app
COPY ./static ./static
COPY ./templates ./templates
COPY ./weights ./weights
COPY requirements.txt .

# 파이썬 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# 애플리케이션 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
