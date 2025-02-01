from hardware.displays.LCD_16x2_display import LCDDisplay
from utils.json_reader import read_json
from utils.configuration import get_hardware_config
from utils.custom_logger import get_logger

# Initialize the logger
logger = get_logger(__name__)


class FaceDisplay:
    def __init__(self):
        """
        Initialize the FaceDisplay object.
        """
        self._hardware_config = get_hardware_config()
        self._expressions = self._get_expressions()
        self._lcd = self._get_lcd()


    def _get_expressions(self):
        """
        Lazily load and return the face expressions.
        """
        logger.debug("Loading face expressions...")
        expressions = read_json("face_display/expressions.json")
        if expressions is None:
            logger.critical("Failed to load face expressions.")
            raise RuntimeError("Face expressions not available.")
        return expressions


    def _get_lcd(self):
        """
        Lazily initialize and return the LCD display.
        """
        logger.debug("Initializing LCD display...")
        try:
            I2C_LCD_ADDRESS = self._hardware_config.get("I2C_LCD_ADDRESS", 0x27)
            lcd = LCDDisplay(address=I2C_LCD_ADDRESS)
            logger.info(f"LCD initialized at address {hex(I2C_LCD_ADDRESS)}")
        except Exception as e:
            logger.critical(f"Failed to initialize LCD: {e}")
            raise
        return lcd

    def display_message(self, message: str, duration: int = 5):
        """
        Display a message on the LCD for a fixed duration.

        Args:
            message (str): The message to display.
            duration (int): The duration to display the message (default: 5 seconds).
        """
        try:
            self._lcd.display_timed_message(message, duration)
        except Exception as e:
            logger.critical(f"Unhandled exception while displaying message: {e}")
            

    def _display_face(self, face_type: str, duration: int):
        """
        Display a predefined face expression on the LCD.
        :param face_type: The type of face expression (e.g., "happy", "angry").
        """
        try:
            expressions = self._get_expressions()
            if face_type not in expressions:
                logger.error(f"Face type '{face_type}' not found in expressions.json.")
                return

            lcd = self._get_lcd()
            face_pattern = expressions[face_type]
            face_message = "\n".join(face_pattern[:2])
            if duration:
                lcd.display_timed_message(face_message, duration)
            else:
                lcd.display_message(face_message)
        except Exception as e:
            logger.critical(f"Unhandled exception while displaying face '{face_type}': {e}")


    def display_angry_face(self, duration=None):
        """
        Display the 'angry' face on the LCD.
        """
        self._display_face("angry", duration)


    def display_happy_face(self,duration=None):
        """
        Display the 'happy' face on the LCD.
        """
        self._display_face("happy", duration)


    def display_neutral_face(self,duration=None):
        """
        Display the 'neutral' face on the LCD.
        """
        self._display_face("neutral", duration)


if __name__ == "__main__":
    # Example usage
    face_display = FaceDisplay()

    try:
        # Display a custom message
        face_display.display_message("Hello, World!")

        # Display predefined faces
        face_display.display_happy_face()
        face_display.display_angry_face()
        face_display.display_neutral_face()
    except Exception as e:
        logger.critical(f"Unhandled exception in main: {e}")
