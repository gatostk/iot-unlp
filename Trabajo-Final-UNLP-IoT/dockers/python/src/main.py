import cv2
import time
import logging
import yaml
import os
from yolo_detector import YOLODetector
from rtsp_reader import RTSPReader
from publisher import Publisher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def build_rtsp_url():
    user = os.getenv("RTSP_USER")
    password = os.getenv("RTSP_PASS")
    ip = os.getenv("RTSP_IP")
    port = os.getenv("RTSP_PORT")
    path = os.getenv("RTSP_PATH")

    if not all([user, password, ip, port, path]):
        raise ValueError("Faltan variables RTSP en .env")

    return f"rtsp://{user}:{password}@{ip}:{port}/{path}"

def main():
    config = load_config()

    if config["rtsp_url"] == "ENV":
        rtsp_url = build_rtsp_url()
    else:
        rtsp_url = config["rtsp_url"]

    mqtt_host = config["mqtt"]["host"]
    mqtt_port = config["mqtt"]["port"]
    mqtt_topic = config["mqtt"]["topic"]
    cooldown = config["mqtt"]["cooldown"]

    min_conf = config["detection"]["min_confidence"]

    reader = RTSPReader(rtsp_url)
    detector = YOLODetector(min_conf=min_conf)
    publisher = Publisher(mqtt_host, mqtt_port, cooldown)

    logger.info("Starting YOLO detection loop...")

    while True:
        frame = reader.get_frame()
        if frame is None:
            continue

        detected, bbox, conf = detector.detect(frame)

        if detected:
            published = publisher.publish_image(mqtt_topic, frame, bbox=bbox, confidence=conf)
            if published:
                logger.info(f"Person detected! Conf={conf:.2f}")

        time.sleep(0.01)

if __name__ == "__main__":
    main()