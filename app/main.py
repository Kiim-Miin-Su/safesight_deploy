from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .yolov8_detector import detect_safety_violation

import cv2
import numpy as np

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/detect")
async def detect(file: UploadFile = File(...), task: str = Form(...)):
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    results, violations = detect_safety_violation(img, task)

    # 인코딩해서 감지된 이미지 다시 보내기
    _, encoded_img = cv2.imencode('.jpg', results)
    return JSONResponse(content={
        "violations": violations,
        "image": encoded_img.tobytes().hex()
    })
