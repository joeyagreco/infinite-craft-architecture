import logging
from typing import Optional

from model.Waze import Waze
from repository.BaseSqlRepository import BaseSqlRepository
from repository.PostgresRepository import PostgresRespository


class WazeRepository(BaseSqlRepository, PostgresRespository):
    def __init__(self, *, connection_string: str, logger: logging.Logger):
        self.__logger = logger
        BaseSqlRepository.__init__(self, schema="public", table="waze", primary_key="waze")
        PostgresRespository.__init__(self, connection_string=connection_string, logger=logger)

    def get_wazes(self, limit: Optional[int] = None) -> list[Waze]:
        return self._get_rows(schema=self._schema, table=self._table, obj_class=Waze, limit=limit)

    def insert_wazes(self, wazes: list[Waze], do_nothing_on_conflict: bool = False) -> int:
        query, values = self._build_insert_query(
            rows=wazes, do_nothing_on_conflict=do_nothing_on_conflict
        )
        cursor = self._execute_query(query, values)
        return cursor.rowcount
