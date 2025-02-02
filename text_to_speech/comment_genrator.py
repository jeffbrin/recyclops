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
        logger.error(f"Invalid result_type: {
                     result_type}. Must be 'correct' or 'incorrect'.")
        raise ValueError(f"Invalid result_type: {
                         result_type}. Must be 'correct' or 'incorrect'.")

    responses = read_json("text_to_speech/responses.json")
    return random.choice(responses[result_type.value])
