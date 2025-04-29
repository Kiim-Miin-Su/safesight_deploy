# 1. Python slim 이미지 사용
FROM python:3.9-slim

# 2. 시스템 라이브러리 설치 (OpenCV 필수 라이브러리)
RUN apt-get update && apt-get install -y \
    libgl1 libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. 코드 복사
COPY ./app ./app
COPY ./static ./static
COPY ./weights ./weights
COPY requirements.txt .

# 5. 파이썬 패키지 설치
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6. 포트 오픈
EXPOSE 8000

# 7. 서버 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
