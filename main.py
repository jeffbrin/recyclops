import os
import time
from object_tracking.object_tracker import ObjectTracker
from utils.custom_logger import get_logger
from face_display.face_display import FaceDisplay
from hardware.cameras.imx500_camera import IMX500Camera
from material_recognition import OpenAIClient

# Initialize the logger
logger = get_logger(__name__)


def main():

    """
    Main function to continuously scan for objects, capture images, 
    and process them before returning to scanning.
    """
    logger.info("Starting object detection system...")
    
    client = OpenAIClient(model="gpt-4o-mini")
    
    tracker = ObjectTracker(detection_distance=10)
    

    try:
        while True:
            # Scan for a new object
            image_path = tracker.scan_for_new_object()
            
            if image_path:
                logger.info(f"Captured image: {image_path}")
                # Process the captured image
                
                response_objects = client.prompt(filepath)
                
                detected_object = tracker.process_latest_image()
                logger.info(f"Detected Object: {detected_object}")

                # Simulate further processing or display results
                print(f"Object recognized: {detected_object}")

                # Simulated delay before resuming scanning (Optional)
                logger.info("Processing complete. Returning to scanning mode.")

    except KeyboardInterrupt:
        logger.info("Shutting down system...")
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
    finally:
        tracker.cleanup()

if __name__ == "__main__":
    main()
