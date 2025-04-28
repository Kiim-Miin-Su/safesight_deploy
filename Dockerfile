FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# safesight_api에서 weights 제외하고 복사
COPY safesight_api/*.py ./
COPY safesight_api/static ./static
COPY safesight_api/templates ./templates

# weights는 복사하지 않음!
# (필요하면 나중에 서버에서 따로 다운로드)

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
