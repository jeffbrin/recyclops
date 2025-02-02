import os
import subprocess
from utils.custom_logger import get_logger
import time

from PIL import Image
from picamera2 import Picamera2

# Initialize the logger
logger = get_logger(__name__)

class IMX500Camera:
    def __init__(self, image_path="captured_images/"):
        """
        Initialize the IMX500 AI Camera.
        :param image_path: Directory where images will be saved.
        """
        try:
            self.image_path = image_path
            os.makedirs(image_path, exist_ok=True)  # Ensure directory exists

            # create fast camera and configure
            self.picam2 = Picamera2()
            self.picam2.configure(self.picam2.create_still_configuration(
                main={"format": 'RGB888', "size": (1000, 1000)}))

            # Check if libcamera is available
            result = subprocess.run(["which", "libcamera-still"], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception("libcamera-still is not installed or not found.")

            logger.info("IMX500 Camera initialized using libcamera")
        except Exception as e:
            logger.error(f"Error initializing IMX500 Camera: {e}")

    def capture_image(self, filename="object.jpg"):
        """
        Capture an image using libcamera-still and save it.
        :param filename: Name of the image file.
        :return: Full path to the saved image.
        """
        try:
            filepath = os.path.join(self.image_path, filename)
            
            # Capture the image using libcamera-still
            command = ["libcamera-still", "-o", filepath, "--nopreview"]
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode != 0:
                raise Exception(f"Failed to capture image: {result.stderr}")

            logger.info(f"Image saved at: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error capturing image: {e}")
            return None
        
    def capture_image_no_file(self) -> Image.Image:
        """
        Captures an image, stores it in memory and returns it as a PIL.Image.Image object.
        """
        
        self.picam2.configure(self.capture_config)

        self.picam2.start()
        return self.picam2.capture_image()

    def cleanup(self):
        """
        Placeholder for any cleanup operations if needed.
        """
        logger.info("IMX500 Camera cleanup complete.")

if __name__ == "__main__":
    cam = IMX500Camera()

    try:
        img_path = cam.capture_image("test_object.jpg")
        if img_path:
            print(f"Image saved: {img_path}")
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
    finally:
        cam.cleanup()
