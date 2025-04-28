@echo off
docker build -t safesight .
docker run -p 8000:8000 -p 8002:8002 safesight
pause
