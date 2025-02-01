import json

class ResponseComponent:
    """
    Object representing the components returned by the OpenAI API text.
    
    Contains the following fields:
    - component_name
    - material
    - recycling_number
    - disposable_category
    """

    component_name: str
    material: str
    recycling_number: str
    disposable_category: str

    def __init__(self, component: dict) -> None:
        self.component_name = component['component_name']
        self.material = component['material']
        try:
            self.recycling_number = component['recycling_number']
        except KeyError:
            pass
        self.disposable_category = component['disposable_category']

def parse_api_response(chatgpt_response_message: str) -> list[ResponseComponent]:
        """
        Takes the output of a chatgpt message and parses it.

        Parameters
        ----------
        chatgpt_response_message : str
            The input should be in the following format:
            Ex:
                [
                    {
                        "component_name": "Bottle",
                        "material": "Plastic",
                        "recycling_number": "7",
                        "disposable_category": "Recycling"
                    },
                    {
                        "component_name": "Cap",
                        "material": "Plastic",
                        "recycling_number": "5",
                        "disposable_category": "Recycling"
                    },
                    {
                        "component_name": "Sticker",
                        "material": "Adhesive Paper/Plastic Mix",
                        "disposable_category": "Garbage"
                    }
                ]
        """

        json_list = json.loads(chatgpt_response_message)
        return [ResponseComponent(obj) for obj in json_list]

