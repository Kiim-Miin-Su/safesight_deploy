FROM python:3.9-slim

WORKDIR /app

# ✅ OpenCV 관련 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Python 종속성 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 프로젝트 복사
COPY . .

# 실행 스크립트 실행
CMD ["bash", "start.sh"]
