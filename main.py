import random
from object_tracking.object_tracker import ObjectTracker
from utils.custom_logger import get_logger
from face_display.face_display import FaceDisplay
from text_to_speech.comment_genrator import get_comment, ResultType
from text_to_speech.tts import TextToSpeech
from text_to_speech.response_to_text_converter import turn_response_to_text
from material_recognition import OpenAIClient
from scoreboard.scoreboard import Scoreboard
import random

# Initialize the logger
logger = get_logger(__name__)


def main():

    """
    Main function to continuously scan for objects, capture images, 
    and process them before returning to scanning.
    """
    logger.info("Starting object detection system...")
    tracker = ObjectTracker(detection_distance=10)
    client = OpenAIClient(model="gpt-4o-mini")
    face_display = FaceDisplay()
    scoreboard =Scoreboard()

    

    try:
        while True:
            # Scan for a new object
            image_path = tracker.scan_for_new_object()
            
            if image_path:
                logger.info(f"Captured image: {image_path}")
                # Process the captured image
                response_objects = client.prompt(image_path)

                # Tell the user what the object is and where to put it
                suggestions = turn_response_to_text(response_objects)

                # Turn suggestions to speech
                for suggestion in suggestions:
                    tts = TextToSpeech()
                    tts.speak(suggestion)

                # Track the object

                # Check that the object was put in the right place
                result = random.choice([ResultType.CORRECT, ResultType.INCORRECT])

                #update and display scoreboard
                components,user_bin_results = scoreboard.generate_dummy_data()
                for i in range(0,len(components)):
                    scoreboard.log_sorting_results(components[i],user_bin_results[i])
                scoreboard.display_total_stats()
                
                # Display the face
                face_display.display_happy_face() if result == ResultType.CORRECT else face_display.display_angry_face()

                # Generate a comment based on the result
                comment = get_comment(result)

                # Turn comment to speech
                for sentence in comment:
                    tts = TextToSpeech()
                    tts.speak(sentence)

                # Make face neutral
                face_display.display_neutral_face()



    except KeyboardInterrupt:
        logger.info("Shutting down system...")
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
    finally:
        tracker.cleanup()
        scoreboard.close_connection()

if __name__ == "__main__":
    main()
