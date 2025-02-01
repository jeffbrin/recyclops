from .promptoutput import PromptOutput

from base64 import b64encode

def base64_encode_image_from_file(image_path: str) -> bytes:
        with open(image_path, "rb") as image_file:
            return b64encode(image_file.read()).decode('utf-8')
