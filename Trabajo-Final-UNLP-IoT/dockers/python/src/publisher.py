import paho.mqtt.client as mqtt
import base64
import cv2
import time
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class Publisher:
    def __init__(self, host, port, cooldown):
        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        self.connected = False
        self.cooldown = cooldown
        self.last_publish = 0

        logger.info(f"[MQTT] Connecting to {host}:{port}")
        self.client.connect(host, port, 60)
        self.client.loop_start()

        for _ in range(20):
            if self.connected:
                break
            time.sleep(0.1)

    def on_connect(self, client, userdata, flags, rc):
        logger.info(f"[MQTT] Connected with code {rc}")
        self.connected = True

    def on_disconnect(self, client, userdata, rc):
        logger.warning(f"[MQTT] Disconnected with code {rc}")
        self.connected = False

    def resize_frame(self, frame):
        max_width = 1280
        max_height = 720

        h, w = frame.shape[:2]
        scale = min(max_width / w, max_height / h)

        if scale < 1:
            new_w = int(w * scale)
            new_h = int(h * scale)
            frame = cv2.resize(frame, (new_w, new_h))
            logger.info(f"[Publisher] Frame resized to {new_w}x{new_h}")

        return frame

    def draw_detection(self, frame, bbox, confidence):
        x1, y1, x2, y2 = bbox

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        hora = datetime.now().strftime("%H:%M:%S")
        label = f"Conf: {confidence:.2f} - {hora}"

        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 255, 0), 2)

        return frame

    def publish_image(self, topic, frame, bbox=None, confidence=None):
        now = time.time()
        if now - self.last_publish < self.cooldown:
            return False

        self.last_publish = now

        if not self.connected:
            logger.warning("[MQTT] Not connected, skipping publish")
            return False

        if bbox is not None and confidence is not None:
            frame = self.draw_detection(frame, bbox, confidence)

        frame = self.resize_frame(frame)

        success, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        if not success:
            logger.error("[Publisher] Failed to encode JPEG")
            return False

        encoded = base64.b64encode(buffer).decode("utf-8")

        payload = {
            "image": encoded,
            "confidence": float(confidence) if confidence is not None else None,
            "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.client.publish(topic, json.dumps(payload), qos=1)

        logger.info("[MQTT] Image + metadata published successfully")
        return True