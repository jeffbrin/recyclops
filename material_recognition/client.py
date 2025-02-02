from dotenv import load_dotenv
import os

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

from .utils import base64_encode_image_from_file
from .prompt_output import parse_api_response, ResponseComponent


class OpenAIClient(OpenAI):

    client: OpenAI
    PROMPT_TEMPLATE: str = """
Instructions:
- Analyze the provided image, which represents an item to be disposed of.
- Each item may have multiple components (e.g., a cup and a lid).
- Determine each visibile components that compose the image, for example, a cup and a lid.
- For each component, determine what material it is.
- If you can recognize the brand of the product and is certain of what recycling number it is, return the recycling number
- For each material, Classify each component as Recycling, Garbage, Compost or Edge case, based on the waste management rules of {0}.
 
Questions:
- For each component in the image, determine wheter it belongs to recycling, Garbage, Compost, or Edge Case.
Format:

Return Format:
- Return only a list of JSON objects, where each object maps a component name, a description of the component, the material and the disposable category. Only return
the JSON objects absolutely no prose. Do not include ```json to start or ``` to end."""

    PART_PROMPT_TEMPLATE: str = """
Instructions:
- Analyze the provided image, which represents an item that was disposed of.
- Each image should only contain one component.
- Determine which of the possible components is present in the photo.
 
Questions:
- Using the image of the entire object as a reference, tell me what component of the object is in the current image.

Return Format:
- Return a single string containing the name of the component and nothing else. The only exception is when you can't identify
the object, in which case, answer with "Unidentified"."""

    def __init__(self, municipality: str = "Montreal", model: str = "gpt-4o", temperature: int = 1, max_tokens: int = 1024):
        load_dotenv(".env")
        api_key = os.environ.get("API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.municipality = municipality

    def _prompt_model(self, image_bytes: bytes) -> list[ResponseComponent]:
        """
        Prompts the model and returns a list of ResponseComponents containing relevant data created by the model.

        Parameters
        ----------
        image_bytes : bytes
            The base64 encoded bytes generated from the image to send to the api.

        Returns
        -------
        list[ResponseComponent]
            A list of ResponseComponent objects containing relevant data created from the model.
        """
        response: ChatCompletion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self._generate_prompt(),
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_bytes}"},
                        },
                    ],
                }
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        return parse_api_response(response.choices[0].message.content)
    
    def _prompt_model_for_individual_part(self, image_bytes: bytes) -> str:
        """
        Prompts the model and returns a list of ResponseComponents containing relevant data created by the model.

        Parameters
        ----------
        image_bytes : bytes
            The base64 encoded bytes generated from the image to send to the api.

        Returns
        -------
        str.
            I string containing the name of the item the openai api thinks was in the image.
        """
        response: ChatCompletion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self._generate_individual_item_prompt(),
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_bytes}"},
                        },
                    ],
                }
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        return response.choices[0].message.content

    def _generate_individual_item_prompt(self) -> str:
        """
        Generates a prompts from the prompt template.

        Returns
        -------
        str
            A string containing instructions to send to the model/
        """
        return OpenAIClient.PART_PROMPT_TEMPLATE

    def _generate_prompt(self) -> str:
        """
        Generates a prompts from the prompt template and municipality.

        Returns
        -------
        str
            A string containing instructions to send to the model/
        """
        return OpenAIClient.PROMPT_TEMPLATE.format(self.municipality)

    def prompt(self, image_path: str) -> list[ResponseComponent]:
        """
        Prompts the OpenAI api and returns a list of ResponseComponent objects containing data generated
        by the model.

        Parameters
        ----------
        image_path : str
            The path to the image to use for the prompt.

        Returns
        -------
        list[ResponseComponent]
            A list of ResponseComponent objects containing relevant data generated by the model.
        """
        image_bytes = base64_encode_image_from_file(image_path)
        return self._prompt_model(image_bytes)
    
    def prompt_which_part(self, part_image_path: str) -> list[ResponseComponent]:
        image_bytes = base64_encode_image_from_file(part_image_path)
        return self._prompt_model_for_individual_part(image_bytes)
