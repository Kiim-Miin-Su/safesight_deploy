from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from yolov8_detector import detect_safety_violation, set_current_task, load_models
import cv2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models = load_models()
camera = cv2.VideoCapture(0)

@app.post("/set_task")
async def set_task(task: str = Form(...)):
    set_current_task(task)
    print(f"🛠️ 작업 설정됨: {task}")
    return {"message": f"{task} 작업 설정 완료"}

@app.get("/video_feed")
def video_feed():
    def gen_frames():
        while True:
            success, frame = camera.read()
            if not success:
                continue
            result = detect_safety_violation(frame, set_current_task(), models)
            for box in result.get("boxes", []):
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, "Not Wearing", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    return StreamingResponse(gen_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
