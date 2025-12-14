import cv2
import logging

logger = logging.getLogger(__name__)

class RTSPReader:
    def __init__(self, rtsp_url):
        if not rtsp_url or rtsp_url.strip() == "":
            logger.error("[RTSP] ERROR: rtsp_url está vacío en config.yaml")
            raise ValueError("rtsp_url vacío")

        self.cap = cv2.VideoCapture(rtsp_url)

        if not self.cap.isOpened():
            logger.error(f"[RTSP] No se pudo abrir la cámara: {rtsp_url}")
            raise RuntimeError("No se pudo abrir RTSP")

        logger.info("[RTSP] Cámara conectada correctamente")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            logger.warning("[RTSP] No se pudo leer frame")
            return None
        return frame