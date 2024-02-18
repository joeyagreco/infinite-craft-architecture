from __future__ import annotations

from dataclasses import dataclass

from enumeration.OpenAiRole import OpenAiRole
from model.abstract.DictSerializable import DictSerializable


@dataclass(kw_only=True)
class OpenAiMessage(DictSerializable):
    role: OpenAiRole
    content: str

    def to_dict(self) -> dict:
        return {"role": self.role.name.lower(), "content": self.content}
