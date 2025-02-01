import os
import cv2
import time
from utils.custom_logger import get_logger

# Initialize the logger
logger = get_logger(__name__)

class IMX500Camera:
    def __init__(self, camera_id=0, image_path="captured_images/", ai_enabled=True):
        """
        Initialize the IMX500 AI Camera.
        :param camera_id: Camera ID (default is 0 for first camera).
        :param image_path: Directory where images will be saved.
        :param ai_enabled: Enable AI inference on the camera sensor.
        """
        try:
            self.camera_id = camera_id
            self.ai_enabled = ai_enabled
            self.image_path = image_path
            os.makedirs(image_path, exist_ok=True)  # Ensure directory exists

            self.cap = cv2.VideoCapture(self.camera_id)
            if not self.cap.isOpened():
                raise Exception("Failed to initialize IMX500 Camera")

            logger.info(f"IMX500 Camera initialized on ID {camera_id}")
        except Exception as e:
            logger.error(f"Error initializing IMX500 Camera: {e}")
            self.cap = None

    def capture_image(self, filename="object.jpg"):
        """
        Capture an image and save it.
        :param filename: Name of the image file.
        :return: Full path to the saved image.
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
            logger.error(f"Error capturing image: {e}")
            return None

    def detect_object(self):
        """
        Run AI inference on the camera sensor to detect objects.
        :return: Detected object category (mocked for now).
        """
        if not self.ai_enabled:
            logger.warning("AI processing disabled. Skipping detection.")
            return None

        try:
            # Placeholder for actual IMX500 AI inference
            detected_class = "Plastic Bottle"  # Mock result
            logger.info(f"Detected object: {detected_class}")
            return detected_class
        except Exception as e:
            logger.error(f"AI detection error: {e}")
            return None

    def cleanup(self):
        """
        Release the camera resource.
        """
        if self.cap:
            self.cap.release()
            logger.info("IMX500 Camera released.")

if __name__ == "__main__":
    # Example usage
    cam = IMX500Camera(camera_id=0, ai_enabled=True)

    try:
        img_path = cam.capture_image("test_object.jpg")
        if img_path:
            detected_object = cam.detect_object()
            print(f"Detected: {detected_object}")
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
    finally:
        cam.cleanup()
