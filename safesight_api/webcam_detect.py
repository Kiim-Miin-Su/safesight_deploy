import cv2
import time
from yolov8_detector import detect_safety_violation, load_models

# 모델 한 번만 로드
models = load_models()

# 웹캠 열기
cap = cv2.VideoCapture(0)

# 감지 결과 캐시 변수
last_detection_time = 0
last_violations = []

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ 웹캠 프레임 읽기 실패")
        break

    now = time.time()
    if now - last_detection_time > 2.0:
        # YOLO 감지 수행
        result = detect_safety_violation(frame, "고소작업", models)
        last_violations = [(x1, y1, x2, y2, label) for label, [x1, y1, x2, y2] in zip(result["labels"], result["boxes"])]
        last_detection_time = now

    # 마지막 감지 결과 시각화
    for (x1, y1, x2, y2, label) in last_violations:
        color = (0, 0, 255) if "No" in label else (0, 255, 0)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # 화면 출력
    cv2.imshow('SafeSight Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 정리
cap.release()
cv2.destroyAllWindows()
