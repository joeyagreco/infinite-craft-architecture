from __future__ import annotations

from enum import unique

from enumeration.BaseEnum import BaseEnum


@unique
class OpenAiModel(BaseEnum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"

    @staticmethod
    def items() -> list[tuple[OpenAiModel, str]]:
        return [(member, member.name) for member in OpenAiModel]

    @classmethod
    def from_str(cls, s: str) -> OpenAiModel:
        for member, _ in OpenAiModel.items():
            if member.value == s:
                return member
        raise ValueError(f"'{s}' is not a valid OpenAiModel.")
