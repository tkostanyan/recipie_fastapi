from abc import ABC, abstractmethod
from typing import Dict

from openai import OpenAI, AsyncOpenAI
from recipie.conf import settings
import json


class BaseLlm(ABC):
    """
        Abstract Base Class for Large Language Model (LLM) clients.

        This class defines the interface for synchronous and asynchronous methods that must be implemented
        by any LLM client.

        Methods:
            generate(prompt: str):
                Abstract method to be implemented for synchronous LLM prompt generation.

            generate_async(prompt: str):
                Abstract method to be implemented for asynchronous LLM prompt generation.
    """

    @abstractmethod
    def generate(self, prompt: str):
        pass

    @abstractmethod
    async def generate_async(self, prompt: str):
        pass


class OpenAiLlm(BaseLlm):
    """
        OpenAI implementation of the BaseLlm for interacting with OpenAI's API.

        This class provides both synchronous and asynchronous methods to generate responses from OpenAI's
        Large Language Models (LLMs) using prompts.

        Attributes:
            client (OpenAI): The synchronous client for interacting with OpenAI's API.
            async_client (AsyncOpenAI): The asynchronous client for interacting with OpenAI's API.

        Methods:
            generate(prompt: str) -> Dict:
                Generates a response from the OpenAI LLM using the given prompt synchronously.

            generate_async(prompt: str) -> Dict:
                Asynchronously generates a response from the OpenAI LLM using the given prompt.
    """

    def __init__(self):
        """
                Initializes the OpenAiLlm class with synchronous and asynchronous OpenAI clients.

                Both the synchronous and asynchronous clients are initialized with the API key from settings.
        """

        if not settings.OPENAI_KEY:
            raise ValueError("OpenAI API key is missing.")

        if not hasattr(OpenAiLlm, '_client'):
            # Check if already initialized
            OpenAiLlm._client = OpenAI(api_key=settings.OPENAI_KEY)
            OpenAiLlm._async_client = AsyncOpenAI(api_key=settings.OPENAI_KEY)

        self.client = OpenAiLlm._client
        self.async_client = OpenAiLlm._async_client

    def generate(self, prompt: str) -> Dict:
        """
                Generates a response from the OpenAI LLM synchronously using the provided prompt.

                Args:
                    prompt (str): The prompt to be sent to the OpenAI API for generating a response.

                Returns:
                    Dict: The generated response from the LLM in JSON format, or an error message if an exception occurs.

                Raises:
                    Exception: Catches any exception during the interaction with the OpenAI API and returns it as an error.
        """
        # Send the request to OpenAI's API
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=settings.OPENAI_LLM,
            response_format={'type': 'json_object'},
        )

        resp_json = self._extract_response(chat_completion)
        return resp_json

    async def generate_async(self, prompt: str) -> Dict:
        """
            Asynchronously generates a response from the OpenAI LLM synchronously using the provided prompt.

            Args:
                prompt (str): The prompt to be sent to the OpenAI API for generating a response.

            Returns:
                Dict: The generated response from the LLM in JSON format, or an error message if an exception occurs.

            Raises:
                Exception: Catches any exception during the interaction with the OpenAI API and returns it as an error.
        """
        # Send the request to OpenAI's API
        chat_completion = await self.async_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=settings.OPENAI_LLM,
            response_format={'type': 'json_object'},
        )

        resp_json = self._extract_response(chat_completion)
        return resp_json

    def _extract_response(self, chat_completion: Dict) -> Dict:
        """
        Helper method to extract and structure the relevant information from the LLM response.
        """
        return json.loads(chat_completion.choices[0].message.content)
