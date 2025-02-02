import time
import cv2
import numpy as np
from datetime import datetime
from hardware.cameras.imx500_camera import IMX500Camera
from hardware.motion_sensor.ultrasonic_motion_sensor import UltrasonicSensor
from utils.custom_logger import get_logger

# Initialize logger
logger = get_logger(__name__)


class ObjectTracker:
    def __init__(self, detection_distance=10):
        """
        Initializes the object tracking module with an ultrasonic sensor and a camera.
        :param detection_distance: Distance (in cm) to detect an object.
        """
        self.camera = IMX500Camera()
        self.sensor = UltrasonicSensor(
            trigger_distance=detection_distance, callback=self._on_object_detected)
        self.image_ready = False
        self.image_path = None

    def _on_object_detected(self, distance):
        """
        Internal callback triggered when an object is detected.
        Captures an image and marks it as ready for processing.
        """
        logger.info(f"Object detected at {distance} cm. Preparing to capture an image...")
        # Give time for the object to be properly placed
        time.sleep(2)

        self.image_path = self._capture_image()
        if self.image_path:
            # Indicate the image is ready for processing
            self.image_ready = True
            return True
        return False

    def _capture_image(self):
        """
        Captures an image using the IMX500 camera and returns the file path.
        :return: Path to the captured image.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scanned_object_{timestamp}.jpg"
        image_path = self.camera.capture_image(filename)

        if image_path:
            logger.info(f"Image successfully captured: {image_path}")
        else:
            logger.error("Failed to capture image.")

        return image_path

    def process_latest_image(self):
        """
        Runs object recognition on the most recently captured image.
        :return: The name of the detected object.
        """
        detected_object = self.camera.detect_object()
        logger.info(f"Detected object: {detected_object}")
        return detected_object

    def scan_for_new_object(self):
        """
        Continuously waits for an object, captures an image, and returns the image path.
        Only resumes scanning after the previous image is fully processed.
        """
        logger.info("Scanning for an object...")

        while True:
            self.image_ready = False
            self.image_path = None

            # Block execution until an object is detected and captured
            self.sensor.start_monitoring()

            # Wait until the image is marked as ready
            while not self.image_ready:
                time.sleep(0.1)  # Prevent CPU overuse

            logger.info(f"Image ready for processing: {self.image_path}")
            return self.image_path  # Return the image path for further processing

    def cleanup(self):
        """
        Releases resources used by the camera and sensor.
        """
        self.camera.cleanup()
        self.sensor.cleanup()
        logger.info("ObjectTracker resources released.")


if __name__ == "__main__":
    # Example usage
    tracker = ObjectTracker(detection_distance=10)

    try:
        while True:
            image_path = tracker.scan_for_new_object()
            if image_path:
                detected_object = tracker.process_latest_image()
                print(f"Object recognized: {detected_object}")

                # Simulate processing before resuming scanning
                logger.info("Processing completed. Resuming scanning mode.")

    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
    finally:
        tracker.cleanup()
