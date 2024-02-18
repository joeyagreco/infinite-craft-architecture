from __future__ import annotations

from enum import unique

from enumeration.BaseEnum import BaseEnum


@unique
class OpenAiRole(BaseEnum):
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"
    USER = "USER"

    @staticmethod
    def items() -> list[tuple[OpenAiRole, str]]:
        return [(member, member.name) for member in OpenAiRole]

    @classmethod
    def from_str(cls, s: str) -> OpenAiRole:
        s_upper = s.upper()
        for member, member_name in OpenAiRole.items():
            if member_name == s_upper:
                return member
        raise ValueError(f"'{s}' is not a valid OpenAiRole.")
