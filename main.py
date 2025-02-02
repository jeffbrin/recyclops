from object_tracking.object_tracker import ObjectTracker
from utils.custom_logger import get_logger
# from face_display.face_display import FaceDisplay
from material_recognition import OpenAIClient

from time import sleep

# Initialize the logger
logger = get_logger(__name__)


def main():
    logger.info("Starting object detection system...")
    garbage_tracker = ObjectTracker(detection_distance=10)
    openai_client = OpenAIClient(model="gpt-4o-mini")

    try:
        while True:
            # # Scan for a new object
            # image_path = garbage_tracker.scan_for_new_object()
            
            # if image_path:
            #     logger.info(f"Captured image: {image_path}")
            #     # Process the captured image
            #     response_objects = openai_client.prompt(image_path)
                
            #     detected_object = garbage_tracker.process_latest_image()
            #     logger.info(f"Detected Object: {detected_object}")

            #     # Simulate further processing or display results
            #     print(f"Object recognized: {detected_object}")

            #     # Simulated delay before resuming scanning (Optional)
            #     logger.info("Processing complete. Returning to scanning mode.")

            # Look for object in specific locations
            print("Capturing Image")
            image = garbage_tracker.capture_image_no_file()
            print(image)
            input("INPUT")
            


    except KeyboardInterrupt:
        logger.info("Shutting down system...")
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
    finally:
        garbage_tracker.cleanup()

if __name__ == "__main__":
    main()
