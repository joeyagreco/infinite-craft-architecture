import logging

import requests

from client.BaseClient import BaseClient
from enumeration.OpenAiModel import OpenAiModel
from enumeration.OpenAiRole import OpenAiRole
from model.abstract.Alivable import Alivable
from model.client.OpenAiChatCompletion import OpenAiChatCompletion
from model.client.OpenAiMessage import OpenAiMessage
from util.ConfigReader import ConfigReader


class OpenAiClient(BaseClient, Alivable):
    """
    https://platform.openai.com/docs/api-reference
    """

    def __init__(self, *, logger: logging.Logger, api_key: str, chat_completion_model: OpenAiModel):
        super().__init__(logger=logger)
        self.__API_KEY = api_key
        self.__BASE_URL = ConfigReader.get("client", "OPEN_AI_API", "BASE_URL")
        self.__VERSION = ConfigReader.get("client", "OPEN_AI_API", "VERSION")
        self.__COMPLETIONS_ROUTE = ConfigReader.get("client", "OPEN_AI_API", "COMPLETIONS_ROUTE")
        self.__CHAT_ROUTE = ConfigReader.get("client", "OPEN_AI_API", "CHAT_ROUTE")
        self.__MODELS_ROUTE = ConfigReader.get("client", "OPEN_AI_API", "MODELS_ROUTE")
        # Models
        self.__CHAT_COMPLETION_MODEL = chat_completion_model.value

    def alive(self) -> bool:
        try:
            self.get_models()
            return True
        except Exception as e:
            self._logger.warning(f"TEST FAILED: {e}")
            return False

    def name(self) -> str:
        return "open ai client"

    def __get_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.__API_KEY}"}

    def get_models(self) -> list[str]:
        url = f"{self.__BASE_URL}{self.__VERSION}{self.__MODELS_ROUTE}"
        # TODO: return actual model. since this is only used for testing right now, this is fine.
        return self._rest_call(requests.get, url, headers=self.__get_headers()).json()

    def get_chat_completion_from_messages(
        self, messages: list[OpenAiMessage]
    ) -> OpenAiChatCompletion:
        url = f"{self.__BASE_URL}{self.__VERSION}{self.__CHAT_ROUTE}{self.__COMPLETIONS_ROUTE}"
        data = {
            "model": self.__CHAT_COMPLETION_MODEL,
            "messages": [message.to_dict() for message in messages],
        }
        response = self._rest_call(requests.post, url, headers=self.__get_headers(), json=data)
        return OpenAiChatCompletion.from_dict(response.json())

    def get_response_from_prompt(self, prompt: str) -> str:
        messages = [OpenAiMessage(role=OpenAiRole.USER, content=prompt)]
        response = self.get_chat_completion_from_messages(messages)
        return response.completion_text
