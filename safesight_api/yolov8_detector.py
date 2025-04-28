# yolov8_detector.py (conf=0.5 적용 + 디버그 포함)
from ultralytics import YOLO

# 모델 전역 로딩 함수
def load_models():
    return {
        "helmet": YOLO("weights/helmet_best.pt"),
        "vest": YOLO("weights/vest_best.pt"),
        "harness": YOLO("weights/harness_merge_best.pt"),
        "gloves": YOLO("weights/gloves_best.pt"),
        "goggles": YOLO("weights/goggles_best.pt"),
        "mask": YOLO("weights/mask_best.pt"),
        "person": YOLO("weights/person_best.pt")
    }

# 현재 작업명 관리
current_task = "고소작업"

def set_current_task(task=None):
    global current_task
    if task:
        current_task = task
    return current_task

def get_current_task():
    return current_task

# 박스 포함 여부 확인 함수
def is_inside(person_box, item_box, threshold=0.1):
    px1, py1, px2, py2 = person_box.xyxy[0]
    ix1, iy1, ix2, iy2 = item_box.xyxy[0]
    inter_x1 = max(px1, ix1)
    inter_y1 = max(py1, iy1)
    inter_x2 = min(px2, ix2)
    inter_y2 = min(py2, iy2)
    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)
    item_area = (ix2 - ix1) * (iy2 - iy1)
    return inter_area / item_area > threshold if item_area > 0 else False

# 감지 함수
def detect_safety_violation(frame, task_name, models):
    task_requirements = {
        "고소작업": ["helmet", "vest", "harness"],
        "용접작업": ["helmet", "goggles", "gloves"],
        "전기작업": ["gloves", "mask"],
        "기계조작": ["helmet", "vest"],
        "화학물질 취급": ["mask", "goggles"],
        "중장비 운전": ["helmet", "vest", "gloves"]
    }

    required_items = task_requirements.get(task_name, [])

    results = {
        item: models[item](frame, conf=0.5)[0] if item in required_items else None
        for item in ["helmet", "vest", "harness", "gloves", "goggles", "mask"]
    }
    results["person"] = models["person"](frame, conf=0.5)[0]

    person_boxes = [box for box in results["person"].boxes if int(box.cls[0]) == 0]

    # 디버깅
    print("[DEBUG] Detected person:", len(person_boxes))
    for item in required_items:
        item_result = results.get(item)
        count = len(item_result.boxes) if item_result else 0
        print(f"[DEBUG] {item} detected:", count)
        if item_result:
            for box in item_result.boxes:
                print(f"[DEBUG] - {item} conf: {box.conf.item():.2f}")

    labels = []
    boxes = []

    for person_box in person_boxes:
        for item in required_items:
            item_result = results.get(item)
            item_boxes = item_result.boxes if item_result else []
            matched = any(is_inside(person_box, item_box) for item_box in item_boxes)
            if not matched:
                x1, y1, x2, y2 = map(int, person_box.xyxy[0])
                labels.append(f"No {item}")
                boxes.append([x1, y1, x2, y2])

    return {
        "labels": labels,
        "boxes": boxes,
        "violation_count": len(labels),
        "message": "✅ 모든 장비 착용 확인됨!" if not labels else "❌ 미착용 장비 있음!"
    }
