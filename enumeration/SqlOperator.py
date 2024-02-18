from __future__ import annotations

from enumeration.BaseEnum import BaseEnum


class SqlOperator(BaseEnum):
    """
    SQL comparison operators.
    """

    EQUAL = "="
    IN = "IN"
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    LIKE = "LIKE"
    NOT_LIKE = "NOT LIKE"

    @staticmethod
    def items() -> list[tuple[SqlOperator, str]]:
        return [(member, member.name) for member in SqlOperator]

    @classmethod
    def from_str(cls, s: str) -> SqlOperator:
        raise NotImplementedError(f"Not a valid method for this enum.")
