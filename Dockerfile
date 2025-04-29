# 1. 가벼운 python 3.9-slim 기반
FROM python:3.9-slim

# 2. 필요한 라이브러리만 최소 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 3. 작업 디렉토리 지정
WORKDIR /app

# 4. requirements 먼저 복사하고 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 5. 코드 복사
COPY ./app ./app

# 6. uvicorn으로 FastAPI 서버 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
