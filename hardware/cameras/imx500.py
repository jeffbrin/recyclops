import time
import os
import cv2
import numpy as np
from utils.custom_logger import get_logger

# Initialize the logger
logger = get_logger(__name__)

class AICamera:
    def __init__(self, camera_id=0, image_path="captured_images/", ai_enabled=True):
        """
        Initialize the AI camera module.
        :param camera_id: Camera ID (default is 0 for first camera).
        :param image_path: Directory where images will be saved.
        :param ai_enabled: Enable on-camera AI processing if available.
        """
        try:
            self.camera_id = camera_id
            self.ai_enabled = ai_enabled
            self.image_path = image_path

            # Create the image directory if it doesn't exist
            os.makedirs(image_path, exist_ok=True)

            # Initialize the camera
            self.cap = cv2.VideoCapture(self.camera_id)
            if not self.cap.isOpened():
                raise Exception("Failed to initialize camera")

            logger.debug(f"IMX500 AI Camera initialized on ID {camera_id}")
        except Exception as e:
            logger.error(f"Error initializing AI camera: {e}")
            self.cap = None

    def capture_image(self, filename="object.jpg"):
        """
        Capture an image from the camera and save it.
        :param filename: Name of the file to save the image.
        :return: Full path of the saved image.
        """
        if self.cap is None:
            logger.error("Camera not initialized. Cannot capture image.")
            return None

        try:
            ret, frame = self.cap.read()
            if not ret:
                raise Exception("Failed to capture frame")

            filepath = os.path.join(self.image_path, filename)
            cv2.imwrite(filepath, frame)
            logger.info(f"Image saved at: {filepath}")

            return filepath
        except Exception as e:
            logger.e
