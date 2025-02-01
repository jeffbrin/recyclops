from object_tracking.object_tracker import ObjectTracker
from utils.custom_logger import get_logger
from hardware.cameras.imx500 import IMX500Camera
# Initialize the logger
logger = get_logger(__name__)


def main():
    # # Look for the object at the object
    # tracker = ObjectTracker()

    # try:
    #     # Capture Image
    #     img_path = tracker.get_object_image("scanned_item.jpg")
        
    #     if img_path:
    #         # Run Object Detection
    #         detected_object = tracker.detect_object()
    #         print(f"Detected Object: {detected_object}")

    #         # Track Object Movement
    #         bin_id = tracker.track_object_to_bin(None)
    #         print(f"Object placed in: {bin_id}")

    # except Exception as e:
    #     logger.critical(f"Unhandled exception: {e}")
    # finally:
    #     tracker.cleanup()
    cam = IMX500Camera()

    try:
        img_path = cam.capture_image("test_object.jpg")
        if img_path:
            detected_object = cam.detect_object()
            print(f"Detected: {detected_object}")
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
    finally:
        cam.cleanup()


    # Identify the object materials

    # Track the object

    # Get the result

    # Display face based on result

    # Generate comment

    # Turn comment to speech

    # Make face neutral

if __name__ == "__main__":
    main()