from __future__ import annotations

from dataclasses import dataclass

from model.abstract.DictDeserializable import DictDeserializable


@dataclass(frozen=True, kw_only=True)
class OpenAiImageGeneration(DictDeserializable):
    revised_prompt: str
    url: str

    @staticmethod
    def from_dict(d: dict) -> OpenAiImageGeneration:
        return OpenAiImageGeneration(
            revised_prompt=d["data"][0]["revised_prompt"], url=d["data"][0]["url"]
        )
