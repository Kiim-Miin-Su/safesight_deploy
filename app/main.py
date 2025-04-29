from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import numpy as np
import cv2
from .yolov8_detector import detect_safety_violation

app = FastAPI()

# Static 파일 연결
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/detect")
async def detect(file: UploadFile = File(...), task: str = Form(...)):
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    annotated_img, violations = detect_safety_violation(img, task)

    # 결과 이미지 인코딩
    _, encoded_img = cv2.imencode('.jpg', annotated_img)

    return JSONResponse(content={
        "violations": violations,
        "image": encoded_img.tobytes().hex()
    })
