from ultralytics import YOLO

MODEL_DICT = {
    "helmet": YOLO("weights/helmet_best.pt"),
    "vest": YOLO("weights/vest_best.pt"),
    "gloves": YOLO("weights/gloves_best.pt"),
    "goggles": YOLO("weights/goggles_best.pt"),
    "harness": YOLO("weights/harness_best.pt"),
    "mask": YOLO("weights/mask_best.pt"),
    "person": YOLO("weights/person_best.pt")
}

TASK_EQUIPMENT_MAP = {
    "고소작업": ["helmet", "harness", "vest"],
    "화학물질 취급 작업": ["mask", "goggles", "gloves"],
    "용접 작업": ["helmet", "gloves", "goggles"],
    "전기 작업": ["helmet", "gloves"],
    "중장비 작업": ["helmet", "vest"],
    "건설 일반": ["helmet", "vest", "gloves"],
}