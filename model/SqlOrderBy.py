from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from enumeration.SqlSortDirection import SqlSortDirection


@dataclass(kw_only=True, eq=False)
class SqlOrderBy:
    expression: str
    sort_direction: Optional[SqlSortDirection] = None
