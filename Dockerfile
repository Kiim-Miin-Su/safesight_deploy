# 베이스 이미지
FROM python:3.9-slim-bullseye

# 작업 디렉토리 설정
WORKDIR /app

# 필수 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 필요한 파일 복사
COPY ./app ./app
COPY ./templates ./templates
COPY ./static ./static
COPY ./weights ./weights
COPY requirements.txt .

# 종속성 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 추가적인 의존성 설치
RUN pip install --no-cache-dir \
    uvicorn \
    fastapi \
    jinja2 \
    aiofiles

# 포트 노출
EXPOSE 8000

# 서버 실행 명령어
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
