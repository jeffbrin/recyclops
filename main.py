import random
from utils.custom_logger import get_logger
from object_tracking.object_tracker import ObjectTracker
from object_tracking.motiondetection import motion_detection
from face_display.face_display import FaceDisplay
from text_to_speech.comment_genrator import get_comment, turn_response_to_text, ResultType
from text_to_speech.speech_manager import TextToSpeechManager
from material_recognition import OpenAIClient

from time import sleep, time

# Initialize the logger
logger = get_logger(__name__)


def main():
    logger.info("Starting object detection system...")
    tracker = ObjectTracker(detection_distance=10)
    client = OpenAIClient(model="gpt-4o-mini")
    face_display = FaceDisplay()
    tts_manager = TextToSpeechManager()

    SCANNING = 0
    TRACKING = 1
    state = SCANNING
    last_image = None
    # TODO: Remove
    # tracking_start_time = time()

    MASK = [[[0, 500], [0, 500]], [[500, 999], [500, 999]]]

    try:
        while True:

            # In the scanning state
            if state == SCANNING:
                # Make face neutral
                face_display.display_neutral_face()

                # Scan for a new object
                image_path = tracker.scan_for_new_object()

                if image_path:
                    logger.info(f"Captured image: {image_path}")
                    
                    # Process the captured image
                    response_objects = client.prompt(image_path)
                    response_objects = list(filter(lambda x: x.component_name is not None, response_objects))

                    # Tell the user what the object is and where to put it
                    instructions = turn_response_to_text(response_objects)

                    # Turn suggestions to speech
                    for instruction in instructions:
                        tts_manager.speak(instruction)

                    # Track the object

                    # Check that the object was put in the right place
                    result = random.choice(
                        [ResultType.CORRECT, ResultType.INCORRECT])

                    # Display the face
                    face_display.display_happy_face(
                    ) if result == ResultType.CORRECT else face_display.display_angry_face()

                    # Generate a comment based on the result
                    comment = get_comment(result)

                    # Turn comment to speech
                    for sentence in comment:
                        tts_manager.speak(sentence)
                        state = TRACKING
                        tracking_start_time = time()

            elif state == TRACKING:
                filename = tracker._capture_image()
                if last_image is None:
                    last_image = filename
                mask_idx = motion_detection(filename, last_image, MASK)
                last_image = filename

                sleep(0.3)

                if mask_idx != -1:
                    items = []
                    for component in response_objects:
                        if component.name not in items:
                            items.append(component.name)
                    component_name = client.prompt_which_part(filename, items)
                    print(component_name)

                # Find better way of going back to previous state
                if time() - tracking_start_time > 10:
                    state = SCANNING
                    last_image = None


    except KeyboardInterrupt:
        logger.info("Shutting down system...")
    except Exception as e:
        import traceback
        print(traceback.print_exception(e))
        logger.critical(f"Unhandled exception: {e}")
    finally:
        tracker.cleanup()


if __name__ == "__main__":
    main()
