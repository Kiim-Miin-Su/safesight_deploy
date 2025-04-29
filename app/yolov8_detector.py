from ultralytics import YOLO
import cv2

# 모델 미리 로드
helmet_model = YOLO("weights/helmet_best.pt")
vest_model = YOLO("weights/vest_best.pt")
goggles_model = YOLO("weights/goggles_best.pt")
harness_model = YOLO("weights/harness_best.pt")
gloves_model = YOLO("weights/gloves_best.pt")
mask_model = YOLO("weights/mask_best.pt")

# 작업별 필요한 장비
TASK_EQUIPMENT_MAP = {
    "고소작업": ["helmet", "vest", "harness"],
    "화학물질 취급 작업": ["mask", "goggles", "gloves"],
    "용접작업": ["helmet", "goggles", "gloves"],
}

MODEL_DICT = {
    "helmet": helmet_model,
    "vest": vest_model,
    "goggles": goggles_model,
    "harness": harness_model,
    "gloves": gloves_model,
    "mask": mask_model,
}

# 감지 함수
def detect_safety_violation(image, task):
    violations = []
    equipments = TASK_EQUIPMENT_MAP.get(task, [])

    # 사람 먼저 감지
    person_model = YOLO("weights/person_best.pt")
    person_results = person_model(image, conf=0.5)[0]
    person_boxes = [p for p in person_results.boxes.xyxy.cpu().numpy()]

    output_image = image.copy()

    for pbox in person_boxes:
        px1, py1, px2, py2 = map(int, pbox)
        missing_items = []

        for equipment in equipments:
            model = MODEL_DICT[equipment]
            detections = model(image, conf=0.5)[0]
            found = False
            for dbox in detections.boxes.xyxy.cpu().numpy():
                x1, y1, x2, y2 = map(int, dbox)
                if px1 <= (x1+x2)//2 <= px2 and py1 <= (y1+y2)//2 <= py2:
                    found = True
                    break
            if not found:
                missing_items.append(equipment)

        if missing_items:
            label = ", ".join(missing_items) + " 미착용"
            cv2.rectangle(output_image, (px1, py1), (px2, py2), (0, 0, 255), 2)
            cv2.putText(output_image, label, (px1, py1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            violations.append(label)

    return output_image, violations
