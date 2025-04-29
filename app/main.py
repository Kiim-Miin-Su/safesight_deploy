import os
import sys

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import cv2
import numpy as np

# 현재 디렉토리 추가 (서버 실행 시 상대 경로 문제 방지)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# yolov8_detector import (주의: 상대 경로 안 쓰고 정상 import)
from yolov8_detector import detect_safety_violation

app = FastAPI()

# static, templates 폴더 mount
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/detect")
async def detect(file: UploadFile = File(...), task: str = Form(...)):
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # YOLO 감지 실행
    results, violations = detect_safety_violation(img, task)

    # 결과 이미지를 다시 인코딩
    _, encoded_img = cv2.imencode('.jpg', results)

    return JSONResponse(content={
        "violations": violations,
        "image": encoded_img.tobytes().hex()
    })
