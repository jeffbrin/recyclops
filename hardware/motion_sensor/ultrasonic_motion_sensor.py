import time
import lgpio
from utils.custom_logger import get_logger
from utils.configuration import get_hardware_config

logger = get_logger(__name__)

class UltrasonicSensor:
    def __init__(self, trig_pin=23, echo_pin=24, trigger_distance=15, callback=None):
        """
        Initializes the ultrasonic sensor.
        :param trig_pin: GPIO pin for the trigger signal.
        :param echo_pin: GPIO pin for receiving the echo signal.
        :param trigger_distance: Distance (in cm) at which to trigger a response.
        :param callback: Function to call when an object is detected.
        """
        self._hardware_config = get_hardware_config()
        self.trig_pin = self._hardware_config.get("TRIG_PIN", trig_pin)
        self.echo_pin = self._hardware_config.get("ECHO_PIN", echo_pin)
        self.trigger_distance = trigger_distance
        self.callback = callback

        # Initialize GPIO chip
        self.chip = lgpio.gpiochip_open(0)

        # Setup GPIO
        lgpio.gpio_claim_output(self.chip, self.trig_pin)  # Trig as OUTPUT
        lgpio.gpio_claim_input(self.chip, self.echo_pin)   # Echo as INPUT

        logger.info(f"Ultrasonic Sensor initialized on TRIG={self.trig_pin}, ECHO={self.echo_pin}")

    def get_distance(self):
        """
        Measures the distance to the nearest object using the ultrasonic sensor.
        :return: Distance in cm.
        """
        # Send trigger pulse
        lgpio.gpio_write(self.chip, self.trig_pin, 1)
        time.sleep(0.00001)  # 10µs pulse
        lgpio.gpio_write(self.chip, self.trig_pin, 0)

        start_time = time.time()
        stop_time = time.time()

        # Wait for echo to start
        while lgpio.gpio_read(self.chip, self.echo_pin) == 0:
            start_time = time.time()

        # Wait for echo to stop
        while lgpio.gpio_read(self.chip, self.echo_pin) == 1:
            stop_time = time.time()

        # Calculate time difference
        elapsed_time = stop_time - start_time

        # Convert to distance (speed of sound is ~343m/s)
        distance = (elapsed_time * 34300) / 2  # Convert to cm

        return round(distance, 2)  # Return rounded distance

    def start_monitoring(self, check_interval=0.5):
        """
        Continuously monitors distance and triggers the callback when an object is detected.
        :param check_interval: Time (in seconds) between distance checks.
        """
        logger.info(f"Starting ultrasonic sensor monitoring... (Trigger distance: {self.trigger_distance} cm)")

        try:
            while True:
                distance = self.get_distance()
                logger.info(f"Measured distance: {distance} cm")

                if distance < self.trigger_distance:
                    logger.info(f"Object detected within {self.trigger_distance} cm!")
                    
                    if self.callback:  # Call the user-defined function
                        self.callback(distance)
                    
                time.sleep(check_interval)  # Wait before next measurement
        except KeyboardInterrupt:
            logger.info("Ultrasonic sensor monitoring stopped.")
        finally:
            self.cleanup()

    def cleanup(self):
        """
        Cleans up GPIO resources.
        """
        lgpio.gpiochip_close(self.chip)  # Close GPIO chip
        logger.info("Ultrasonic Sensor GPIO cleaned up.")

if __name__ == "__main__":
    # Example usage: Define a simple callback function
    def object_detected(distance):
        print(f"Object detected at {distance} cm!")

    # Initialize the ultrasonic sensor with a 10 cm trigger distance
    sensor = UltrasonicSensor(trigger_distance=10, callback=object_detected)
    
    # Start monitoring
    sensor.start_monitoring()
