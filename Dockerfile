FROM python:3.9-slim-bullseye

WORKDIR /app

# 필요한 최소 패키지 설치 (OpenCV 동작용 libGL만 추가)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 코드 복사
COPY ./app ./app
COPY ./static ./static
COPY ./weights/helmet_best.pt ./weights/helmet_best.pt
COPY ./weights/vest_best.pt ./weights/vest_best.pt
COPY ./weights/person_best.pt ./weights/person_best.pt
COPY requirements.txt .

# pip install
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 포트 열기
EXPOSE 8000

# 서버 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
