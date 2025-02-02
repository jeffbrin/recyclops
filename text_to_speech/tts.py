import pyttsx3
import tempfile
import os
from hardware.speakers.USB_speaker import Speaker
from utils.custom_logger import get_logger

# Initialize the logger
logger = get_logger(__name__)

class TextToSpeech:
    def __init__(self, voice_id:int=None, rate:int=150):
        """
        Initialize the TextToSpeech object.

        :param voice_id: Voice ID to use. If None, the default voice is used.
        :param rate: Speech rate in words per minute.
        """
        # Initialize the TTS engine and audio player
        try:
            self.engine = pyttsx3.init()
            self.set_rate(rate)
            if voice_id is not None:
                self.set_voice(voice_id)
            logger.info("TextToSpeech engine initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            self.engine = None

        # Initilaize the speaker
        self.speaker = Speaker()
        self.speaker.set_volume(5.0)

    def set_rate(self, rate:int):
        """
        Set the speech rate of the TTS engine.

        :param rate: Speech rate in words per minute.
        """
        if self.engine:
            self.engine.setProperty('rate', rate)
            logger.info(f"Speech rate set to {rate} words per minute.")

    def set_voice(self, voice_id:int):
        """
        Set the voice of the TTS engine.
        :param voice_id: Voice ID to use.
        """
        if self.engine:
            voices = self.engine.getProperty('voices')
            if 0 <= voice_id < len(voices):
                self.engine.setProperty('voice', voices[voice_id].id)
                logger.info(f"Voice set to ID {voice_id}.")
            else:
                logger.warning(f"Invalid voice ID {voice_id}. Using default voice.")

    def speak(self, text:str):
        """
        Speak the given text using the TTS engine.

        :param text: Text to speak.
        """
        if self.engine:
            try:
                logger.info(f"Speaking text: {text}")

                # Save the TTS output to a temporary WAV file
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav_file:
                    temp_wav_path = temp_wav_file.name
                    self.engine.save_to_file(text, temp_wav_path)
                    self.engine.runAndWait()
                    logger.info(f"TTS output saved to {temp_wav_path}")

                # Play the generated WAV file
                self.speaker.play(temp_wav_path)
                logger.info("TTS output played.")

                # Clean up temporary file
                os.remove(temp_wav_path)
                logger.info("Temporary WAV file removed.")
            except Exception as e:
                logger.error(f"Error during speech synthesis or playback: {e}")


if __name__ == "__main__":
    tts = TextToSpeech(voice_id=0, rate=150)

    tts.speak("Hello, World!")
    tts.speak("Great job! You're a recycling wizard.")
