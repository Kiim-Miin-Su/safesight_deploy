# main.py
from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from yolov8_detector import detect_safety_violation, load_models, set_current_task, get_current_task

app = FastAPI()

# CORS 설정 (Django 프론트와 연동 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# YOLO 모델 로드
models = load_models()

# 아이폰 카메라 (2번 인덱스) 고정 열기
camera = cv2.VideoCapture(1)
if not camera.isOpened():
    print("Warning: Camera not available. Sending black frames instead.")
    camera = None

# 최근 감지 결과 저장용
latest_violation_result = {"message": "", "labels": [], "boxes": [], "violation_count": 0}


# 업로드된 이미지 파일 읽기
def read_imagefile(file) -> np.ndarray:
    return cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)


# 작업(task) 설정 API
@app.post("/set_task")
async def set_task(task: str = Form(...)):
    set_current_task(task)
    return {"message": f"{task} 작업으로 설정되었습니다."}


# 현재 상태(status) 반환 API
@app.get("/get_status")
async def get_status():
    return latest_violation_result


# 실시간 영상 스트리밍 API
@app.get("/video_feed")
def video_feed():
    def gen_frames():
        global latest_violation_result
        while True:
            if camera:
                success, frame = camera.read()
                if not success:
                    # 카메라 연결은 됐지만 읽기 실패 → 검은 화면
                    frame = np.zeros((480, 640, 3), dtype=np.uint8)
            else:
                # 아예 카메라가 없으면 검은 화면
                frame = np.zeros((480, 640, 3), dtype=np.uint8)

            task_name = get_current_task()
            result = detect_safety_violation(frame, task_name, models)
            latest_violation_result = result

            # 미착용 감지된 박스 그리기
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
