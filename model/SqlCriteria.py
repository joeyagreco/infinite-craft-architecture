from __future__ import annotations

from dataclasses import dataclass

from enumeration.SqlOperator import SqlOperator


@dataclass(kw_only=True, eq=False)
class SqlCriteria:
    sql_operator: SqlOperator
    column_name: str
    value: any
