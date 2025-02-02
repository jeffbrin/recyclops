import logging
import os

# Define color codes
RESET = "\033[0m"
RED = "\033[31m"
YELLOW = "\033[33m"


class ColorFormatter(logging.Formatter):
    def format(self, record):
        log_msg = super().format(record)
        if record.levelno == logging.ERROR:
            return f"{RED}{log_msg}{RESET}"
        elif record.levelno == logging.WARNING:
            return f"{YELLOW}{log_msg}{RESET}"
        return log_msg


def get_logger(name):
    """
    Creates and returns a logger with both stream and file handlers.

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Ensure the logs directory exists in the project root
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), ".."))
    log_folder = os.path.join(project_root, "logs")
    os.makedirs(log_folder, exist_ok=True)

    # Log debug messages to a file
    file_handler = logging.FileHandler(os.path.join(log_folder, "debug.log"))
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Log colored messages to the console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_formatter = ColorFormatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    return logger


# Example usage for testing purposes
if __name__ == "__main__":
    LOGGER = get_logger(__name__)
    LOGGER.debug("This is a debug message")
    LOGGER.info("This is an info message")
    LOGGER.warning("This is a warning message")
    LOGGER.error("This is an error message")
