import random
from enum import Enum
from utils.json_reader import read_json
from utils.custom_logger import get_logger

# Initialize the logger
logger = get_logger(__name__)


class ResultType(Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"


def get_comment(result_type: ResultType):
    """
    Get a random comment based on the result type (correct or incorrect).
    :param result_type: ResultType Enum (CORRECT or INCORRECT)
    :return: A random comment as a string.
    """
    if not isinstance(result_type, ResultType):
        logger.error(f"Invalid result_type: {result_type}. Must be 'correct' or 'incorrect'.")
        raise ValueError(f"Invalid result_type: {result_type}. Must be 'correct' or 'incorrect'.")

    responses = read_json("text_to_speech/responses.json")
    return random.choice(responses[result_type.value])

def turn_response_to_text(response_objects):
    """
    Converts OpenAI response objects into user-friendly spoken instructions.

    :param response_objects: List of ResponseComponent objects.
    :return: List of formatted instructional strings.
    """
    instructions = []

    for obj in response_objects:
        # Validate that all expected attributes exist
        if not hasattr(obj, "component_name") or not hasattr(obj, "material") or not hasattr(obj, "disposable_category"):
            logger.error("Response object is missing expected attributes.")
            instructions.append("There was an issue understanding this item. Please try again.")
            continue  # Skip this object and move to the next

        # Extract values, handling None cases
        component_name = obj.component_name if obj.component_name else "an unknown object"
        material = obj.material if obj.material else "an unknown material"
        recycling_number = f" with recycling number {obj.recycling_number}" if obj.recycling_number else ""
        disposable_category = obj.disposable_category if obj.disposable_category else "an unknown category"

        # Construct message
        message = f"It looks like you have {component_name}, made of {material}{recycling_number}. Please put it in {disposable_category}. If that is not what you have, please pull it away and present it again."
        instructions.append(message)

    return instructions

