# 베이스 이미지
FROM python:3.9

# 작업 디렉토리 생성
WORKDIR /app

# 필요 파일 복사
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY safesight_api/ .

# FastAPI 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
