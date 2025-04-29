# Python 3.9 이미지 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY ./app ./app
COPY ./static ./static
COPY requirements.txt ./requirements.txt

# 패키지 설치
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 포트 개방
EXPOSE 8000

# FastAPI 서버 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]