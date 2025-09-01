import random
from .xcode_templates import XCODE_TEMPLATES

class XCodeManager:
    def __init__(self):
        pass

    def generate_code(self, prompt: str) -> str:
        """
        Generates Swift code based on a prompt.
        """
        prompt = prompt.lower()
        for keyword, template in XCODE_TEMPLATES.items():
            if keyword in prompt:
                return template

        return XCODE_TEMPLATES["default"]
