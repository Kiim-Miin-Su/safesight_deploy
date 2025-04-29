from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .yolov8_detector import MODEL_DICT, TASK_EQUIPMENT_MAP
import io
from PIL import Image
import numpy as np

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/detect")
async def detect(task: str = Form(...), file: UploadFile = Form(...)):
    task_equipment = TASK_EQUIPMENT_MAP.get(task, [])

    contents = await file.read()
    img_pil = Image.open(io.BytesIO(contents)).convert('RGB')
    img = np.array(img_pil)

    detections = []

    person_results = MODEL_DICT["person"](img_pil)
    if not person_results or not person_results[0].boxes.xyxy.numel():
        return {"results": []}

    person_boxes = person_results[0].boxes.xyxy.cpu().numpy().tolist()

    for person_box in person_boxes:
        x1, y1, x2, y2 = [int(v) for v in person_box[:4]]

        missing_items = []
        for item in task_equipment:
            item_model = MODEL_DICT.get(item)
            if not item_model:
                continue

            item_results = item_model(img_pil)
            if not item_results or not item_results[0].boxes.xyxy.numel():
                missing_items.append(item)
                continue

            found = False
            for item_box in item_results[0].boxes.xyxy.cpu().numpy().tolist():
                ix1, iy1, ix2, iy2 = [int(v) for v in item_box[:4]]
                if x1 <= (ix1 + ix2) / 2 <= x2 and y1 <= (iy1 + iy2) / 2 <= y2:
                    found = True
                    break
            if not found:
                missing_items.append(item)

        detections.append({
            "bbox": [x1, y1, x2, y2],
            "missing": missing_items
        })

    return {"results": detections}