# main.py
from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import os
from yolov8_detector import detect_safety_violation, load_models, set_current_task, get_current_task

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# YOLO 모델 로드
models = load_models()

# Cloudtype 서버면 카메라 끔
camera = None
if os.getenv("CLOUD_DEPLOY") != "1":  # 로컬 개발 환경일 때만 카메라 켜기
    camera = cv2.VideoCapture(1)
    if not camera.isOpened():
        print("Warning: Camera not available. Sending black frames instead.")
        camera = None
else:
    print("Cloud deploy detected. Camera disabled.")

latest_violation_result = {"message": "", "labels": [], "boxes": [], "violation_count": 0}


def read_imagefile(file) -> np.ndarray:
    return cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)


@app.post("/set_task")
async def set_task(task: str = Form(...)):
    set_current_task(task)
    return {"message": f"{task} 작업으로 설정되었습니다."}


@app.get("/get_status")
async def get_status():
    return latest_violation_result


@app.get("/video_feed")
def video_feed():
    def gen_frames():
        global latest_violation_result
        while True:
            if camera:
                success, frame = camera.read()
                if not success:
                    frame = np.zeros((480, 640, 3), dtype=np.uint8)
            else:
                frame = np.zeros((480, 640, 3), dtype=np.uint8)

            task_name = get_current_task()
            result = detect_safety_violation(frame, task_name, models)
            latest_violation_result = result

            for box in result.get("boxes", []):
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, "Not Wearing", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return StreamingResponse(gen_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
