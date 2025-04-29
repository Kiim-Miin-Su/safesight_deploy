from ultralytics import YOLO
import cv2

# 모델 로딩
models = {
    "helmet": YOLO("weights/helmet_best.pt"),
    "vest": YOLO("weights/vest_best.pt"),
    "harness": YOLO("weights/harness_best.pt"),
    "gloves": YOLO("weights/gloves_best.pt"),
    "goggles": YOLO("weights/goggles_best.pt"),
    "mask": YOLO("weights/mask_best.pt"),
    "person": YOLO("weights/person_best.pt"),
}

# 작업별 필요한 장비
task_to_equipment = {
    "highplace": ["helmet", "harness", "vest"],
    "welding": ["goggles", "gloves", "mask"],
    "electrical": ["helmet", "gloves"],
}


def detect_safety_violation(image, task_name):
    violation_boxes = []
    required_items = task_to_equipment.get(task_name, [])

    person_result = models["person"](image)
    people_boxes = person_result[0].boxes.xyxy.cpu().tolist()

    detections = {}
    for item in required_items:
        result = models[item](image)
        detections[item] = result[0].boxes.xyxy.cpu().tolist()

    for person_box in people_boxes:
        x1, y1, x2, y2 = map(int, person_box)
        missing_items = []

        for item, boxes in detections.items():
            found = False
            for bx1, by1, bx2, by2 in boxes:
                bx1, by1, bx2, by2 = map(int, (bx1, by1, bx2, by2))
                if (bx1 >= x1 and by1 >= y1 and bx2 <= x2 and by2 <= y2):
                    found = True
                    break
            if not found:
                missing_items.append(item)

        if missing_items:
            label = "no " + ", ".join(missing_items)
            violation_boxes.append((x1, y1, x2, y2, label))

    # 시각화
    annotated = image.copy()
    if violation_boxes:
        # 여러 미착용자가 있어도 첫 번째만 빨간 박스
        x1, y1, x2, y2, label = violation_boxes[0]
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.putText(
            annotated, label, (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2
        )

    return annotated, [box[4] for box in violation_boxes]
