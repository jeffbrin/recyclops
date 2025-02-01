import os
from client import OpenAIClient

client = OpenAIClient(model="gpt-4o-mini")

IMAGE_TESTING_FOLDER = "material_recognition/image_testing"
for file in os.listdir(IMAGE_TESTING_FOLDER):
    filepath = os.path.join(IMAGE_TESTING_FOLDER, file)
    response_objects = client.prompt(filepath)

    for response_obj in response_objects:
        print(response_obj)
