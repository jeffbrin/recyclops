import base64
import os

from openai import OpenAI
from dotenv import load_dotenv

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

load_dotenv()
API_KEY = os.environ.get("API_KEY")
client = OpenAI(api_key=API_KEY)

# Path to your image
image_path = "path_to_your_image.jpg"

# Getting the Base64 string
base64_image = encode_image(image_path)

Municipality = 'Montreal'



prompt = f"""
Instructions:
- Analyze the provided image, which represents an item to be disposed of.
- Each item may have multiple components (e.g., a cup and a lid).
- Determine each visibile components that compose the image, for example, a cup and a lid.
- For each component, determine what material it is.
- If you can recognize the brand of the product and is certain of what recycling number it is, return the recycling number
- For each material, Classify each component as Recycling, Garbage, Compost or Edge case, based on the waste management rules of {Municipality}.
 
Questions:
- For each component in the image, determine wheter it belongs to recycling, Garbage, Compost, or Edge Case.
Format:
- Return only a list of JSON objects, where each object maps a component name, the material and the disposable category. Only return
the JSON objects absolutely no prose."""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ],
)
