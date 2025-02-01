from object_tracking.object_tracker import ObjectTracker
from utils.custom_logger import get_logger
from hardware.cameras.imx500_camera import IMX500Camera
from hardware.motion_sensor.ultrasonic_motion_sensor import UltrasonicSensor
from utils.custom_logger import get_logger

logger = get_logger(__name__)

def object_detected(distance):
    """
    Callback function triggered when an object is detected.
    Captures an image using the IMX500 camera.
    :param distance: The detected distance to the object.
    """
    logger.info(f"Object detected at {distance} cm! Capturing image...")
    
    camera = IMX500Camera()
    img_path = camera.capture_image("detected_object.jpg")
    
    if img_path:
        logger.info(f"Image successfully captured: {img_path}")
    else:
        logger.error("Failed to capture image.")

def main():
    """
    Main entry point: Initializes the ultrasonic sensor and starts monitoring.
    """
    logger.info("Starting object detection system...")

    sensor = UltrasonicSensor(trigger_distance=10, callback=object_detected)

    try:
        sensor.start_monitoring()
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
    finally:
        sensor.cleanup()

if __name__ == "__main__":
    main()