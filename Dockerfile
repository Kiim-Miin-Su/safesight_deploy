# Base image: Python 3.9 slim
FROM python:3.9-slim

# 필요한 시스템 패키지 설치 (OpenCV가 libgl 필요)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리
WORKDIR /app

# requirements.txt 복사
COPY requirements.txt .

# torch는 CPU 버전으로 따로 설치
RUN pip install --no-cache-dir torch==2.0.0+cpu torchvision==0.15.0+cpu torchaudio==2.0.1+cpu --index-url https://download.pytorch.org/whl/cpu

# 나머지 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 포트 오픈
EXPOSE 8000

# FastAPI 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
