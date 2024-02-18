from __future__ import annotations

from enumeration.BaseEnum import BaseEnum


class SqlSortDirection(BaseEnum):
    ASC = "ASC"
    DESC = "DESC"

    @staticmethod
    def items() -> list[tuple[SqlSortDirection, str]]:
        return [(member, member.name) for member in SqlSortDirection]

    @classmethod
    def from_str(cls, s: str) -> SqlSortDirection:
        raise NotImplementedError(f"Not a valid method for SqlSortDirection.")
