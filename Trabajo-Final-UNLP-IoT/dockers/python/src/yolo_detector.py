from ultralytics import YOLO
import cv2

class YOLODetector:
    def __init__(self, model_path="yolov8n.pt", min_conf=0.7):
        self.model = YOLO(model_path)
        self.min_conf = min_conf

    def detect(self, frame):
        results = self.model(frame, verbose=False)[0]

        best_conf = 0
        best_box = None

        for box in results.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            # Solo personas (clase 0)
            if cls == 0 and conf >= self.min_conf:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                if conf > best_conf:
                    best_conf = conf
                    best_box = (x1, y1, x2, y2)

        if best_box is None:
            return False, None, None

        return True, best_box, best_conf