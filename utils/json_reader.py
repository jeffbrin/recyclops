import json
import os
from typing import Any

# Use your custom logger
from utils.custom_logger import get_logger

logger = get_logger(__name__)


def read_json(file_path: str) -> Any:
    """
    Reads a JSON file and returns the parsed data.
    Handles errors and logs them appropriately.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        Any: Parsed JSON data, or None if an error occurs.
    """
    if not os.path.exists(file_path):
        logger.error(f"JSON file not found: {file_path}")
        return None

    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            logger.debug(f"Successfully loaded JSON file: {file_path}")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON file {file_path}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error reading JSON file {file_path}: {e}")

    return None
