import random
from utils.custom_logger import get_logger
from object_tracking.object_tracker import ObjectTracker
from object_tracking.motiondetection import motion_detection, masking
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
    mask_to_region_mapping = {
        0: "Compost",
        1: "Recycling",
        2: "Garbage"
    }

    MASK = [[[1350, 1900], [780, 1450]], [
        [650, 1265], [753, 1440]], [[0, 577], [753, 1450]]]

    items = []
    items_to_bin_mapping = {}
    last_index = -1
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
                    response_objects = list(
                        filter(lambda x: x.component_name is not None and (x.component_name.lower() != "box" and x.material.lower() != "cardboard"), response_objects))
                    items_to_bin_mapping = {obj.component_name.lower(
                    ): obj.disposable_category for obj in response_objects}

                    # Tell the user what the object is and where to put it
                    instructions = turn_response_to_text(response_objects)

                    # Turn suggestions to speech
                    for instruction in instructions:
                        tts_manager.speak(instruction)

                    state = TRACKING
                    tracking_start_time = time()

                    # Items to be detected
                    items = []
                    for component in response_objects:
                        if component.component_name.lower() not in [i.lower() for i in items]:
                            items.append(component.component_name.lower())

            elif state == TRACKING:
                
                filename = tracker._capture_image()
                if last_image is None:
                    last_image = filename
                mask_idx, masked_image_filepath = motion_detection(filename, last_image, MASK, tracker._capture_image)
                last_image = filename

                sleep(0.05)

                # Prompt openai to see what item was placed in the bin
                if mask_idx != -1 and last_index == -1:

                    component_name = client.prompt_which_part(masked_image_filepath, items)
                    tts_manager.speak(
                        f"Detected {component_name} placed in {mask_to_region_mapping[mask_idx]}")

                    # Check that the object was put in the right place
                    result = ResultType.CORRECT if component_name.lower(
                    ) in items_to_bin_mapping and items_to_bin_mapping[component_name.lower()] == mask_to_region_mapping[mask_idx] else ResultType.INCORRECT
                    # result = random.choice(
                    #     [ResultType.CORRECT, ResultType.INCORRECT])

                    # Display the face
                    face_display.display_happy_face(
                    ) if result == ResultType.CORRECT else face_display.display_angry_face()

                    # Generate a comment based on the result
                    comment = get_comment(result)

                    # Turn comment to speech
                    for sentence in comment:
                        tts_manager.speak(sentence)

                # Find better way of going back to previous state
                if time() - tracking_start_time > 45:
                    state = SCANNING
                    last_image = None
                last_index = mask_idx

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
