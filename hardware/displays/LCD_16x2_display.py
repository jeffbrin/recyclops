from time import sleep
from RPLCD.i2c import CharLCD
from utils.custom_logger import get_logger

# Initialize the logger
logger = get_logger(__name__)


class LCDDisplay:
    def __init__(self, address=0x27, bus_type='PCF8574', columns=16, rows=2):
        """
        Initialize the LCD display.
        :param address: I2C address of the LCD.
        :param bus_type: Type of I2C driver (default is 'PCF8574').
        :param columns: Number of columns on the LCD (default is 16).
        :param rows: Number of rows on the LCD (default is 2).
        """
        try:
            self.lcd = CharLCD(bus_type, address, cols=columns, rows=rows)
            self.columns = columns
            self.rows = rows
            logger.info(f"LCD initialized at address {hex(address)}")
        except Exception as e:
            logger.error(f"Failed to initialize LCD: {e}")
            self.lcd = None

    def display_message(self, message, wrap=True):
        """
        Display a message on the LCD, formatted for a 16x2 screen.
        :param message: Text to display. Use \n for manual line breaks.
        :param wrap: Whether to wrap long lines to fit the display (default is True).
        """
        if self.lcd is None:
            logger.error("LCD not initialized. Cannot display message.")
            return

        try:
            # Split the message into lines
            lines = message.split("\n")
            formatted_lines = []

            for line in lines:
                while line:
                    formatted_lines.append(
                        line[:self.columns].ljust(self.columns))
                    line = line[self.columns:] if wrap else ""

            # Combine formatted lines and truncate to the LCD height
            formatted_message = "".join(formatted_lines[:self.rows])
            logger.debug(f"Displaying formatted message:\n{formatted_message}")
            self.lcd.write_string(formatted_message)
        except Exception as e:
            logger.error(f"Error displaying message: {e}")

    def clear(self):
        """
        Clear the LCD screen.
        """
        if self.lcd is None:
            logger.error("LCD not initialized. Cannot clear.")
            return

        try:
            logger.info("Clearing LCD screen")
            self.lcd.clear()
        except Exception as e:
            logger.error(f"Error clearing LCD screen: {e}")

    def display_timed_message(self, message, duration=5):
        """
        Display a message on the LCD for a specific duration, then clear it.
        :param message: Text to display on the LCD.
        :param duration: Time (in seconds) to display the message (default is 5).
        """
        if self.lcd is None:
            logger.error("LCD not initialized. Cannot display timed message.")
            return

        try:
            self.display_message(message)
            sleep(duration)
        except Exception as e:
            logger.error(f"Error displaying timed message: {e}")
        finally:
            self.clear()


if __name__ == "__main__":
    # Example usage
    lcd = LCDDisplay(address=0x27)

    try:
        lcd.display_timed_message("I2C Address 0x27\nHello, World!", 5)
        lcd.display_timed_message(
            "This is a long message that exceeds the capacity\nof a 16x2 display!", 5)
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
