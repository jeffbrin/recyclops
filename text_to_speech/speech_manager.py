import threading
import queue
from text_to_speech.tts import TextToSpeech

class TextToSpeechManager:
    """
    Manages text-to-speech in a background thread to prevent overlapping speech.
    """
    def __init__(self):
        self.tts = TextToSpeech()
        self.speech_queue = queue.Queue()
        self.speaking_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speaking_thread.start()

    def _speech_worker(self):
        """
        Continuously runs in the background to process speech requests one at a time.
        """
        while True:
            text = self.speech_queue.get()  # Get next text from queue
            if text is None:  
                break  # Exit the thread if None is received (cleanup)
            self.tts.speak(text)  # Speak text
            self.speech_queue.task_done()  # Mark task as complete

    def speak(self, text):
        """
        Adds text to the speech queue.
        """
        self.speech_queue.put(text)

    def shutdown(self):
        """
        Stops the speech thread gracefully.
        """
        self.speech_queue.put(None)  # Signal the thread to exit
        self.speaking_thread.join()  # Wait for thread to finish
