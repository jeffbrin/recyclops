from gtts import gTTS
import tempfile
import os
from hardware.speakers.USB_speaker import Speaker
from utils.custom_logger import get_logger

# Initialize the logger
logger = get_logger(__name__)


class TextToSpeech:
    def __init__(self, lang: str = "en", volume: float = 5.0):
        """
        Initialize the TextToSpeech object using Google TTS.

        :param lang: Language code for speech synthesis.
        :param volume: Speaker volume level.
        """
        try:
            self.lang = lang
            self.speaker = Speaker()
            self.speaker.set_volume(volume)
            logger.info("Google TextToSpeech initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Google TTS: {e}")

    def speak(self, text: str):
        """
        Speak the given text using Google TTS.

        :param text: Text to speak.
        """
        try:
            logger.info(f"Speaking text: {text}")

            # Generate speech audio using Google TTS
            tts = gTTS(text=text, lang=self.lang, slow=False)

            # Save the speech output to a temporary audio file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio_file:
                temp_audio_path = temp_audio_file.name
                tts.save(temp_audio_path)
                logger.info(f"TTS output saved to {temp_audio_path}")

            # Play the generated audio file
            self.speaker.play(temp_audio_path)
            logger.info("TTS output played.")

            # Clean up temporary file
            os.remove(temp_audio_path)
            logger.info("Temporary audio file removed.")
        except Exception as e:
            logger.error(f"Error during speech synthesis or playback: {e}")


if __name__ == "__main__":
    tts = TextToSpeech(lang="en")
    tts.speak("Hello, World!")
    tts.speak("Great job! You're a recycling wizard.")
