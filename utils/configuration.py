from utils.custom_logger import get_logger
from utils.json_reader import read_json

# Initialize the logger
logger = get_logger(__name__)


def get_hardware_config():
    """
    Lazily load and return the hardware configuration.
    """
    logger.debug("Loading hardware configuration...")
    hardware_config = read_json("hardware/hardware_config.json")
    if hardware_config is None:
        logger.critical("Failed to load hardware configuration.")
        raise RuntimeError("Hardware configuration not available.")
    return hardware_config
