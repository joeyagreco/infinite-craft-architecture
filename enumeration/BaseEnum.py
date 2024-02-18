from __future__ import annotations

from abc import abstractmethod
from enum import Enum, unique


@unique
class BaseEnum(Enum):
    """
    Should be inherited by all enums.
    """

    ...

    @staticmethod
    @abstractmethod
    def items() -> list[tuple[BaseEnum, str]]:
        ...

    @classmethod
    def from_str(cls, s: str) -> BaseEnum:
        ...
