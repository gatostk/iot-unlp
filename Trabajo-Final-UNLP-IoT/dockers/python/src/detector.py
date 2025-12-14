import cv2
import numpy as np

class Detector:
    def __init__(self, min_movement=5000):
        self.min_movement = min_movement
        self.previous_frame = None

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.previous_frame is None:
            self.previous_frame = gray
            return False

        frame_delta = cv2.absdiff(self.previous_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        movement = np.sum(thresh) / 255

        self.previous_frame = gray

        return movement > self.min_movement