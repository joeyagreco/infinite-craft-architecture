from __future__ import annotations

from dataclasses import dataclass

from model.abstract.DictDeserializable import DictDeserializable


@dataclass(frozen=True, kw_only=True)
class OpenAiChatCompletion(DictDeserializable):
    completion_text: str

    @staticmethod
    def from_dict(d: dict) -> OpenAiChatCompletion:
        return OpenAiChatCompletion(completion_text=d["choices"][0]["message"]["content"])
