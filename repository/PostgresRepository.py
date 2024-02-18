import logging
from functools import wraps
from typing import Optional

import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictCursor

from enumeration.SqlOperator import SqlOperator
from exception.SqlException import SqlException
from model.abstract.DictDeserializable import DictDeserializable
from model.SqlCriteria import SqlCriteria
from model.SqlOrderBy import SqlOrderBy


class PostgresRespository:
    def __init__(self, *, connection_string: str, logger: logging.Logger):
        self.__logger = logger
        self.__connection = None
        self.__connection_string = connection_string

    def connection_required(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.__connect()
            try:
                return func(self, *args, **kwargs)
            finally:
                self.__close()

        return wrapper

    def __connect(self):
        try:
            self.__connection = psycopg2.connect(self.__connection_string)
            self.__logger.debug("Connection to PostgreSQL DB successful")
        except Exception as e:
            self.__logger.error(f"The error '{e}' occurred")

    def __close(self):
        if self.__connection is not None:
            self.__connection.close()
            self.__logger.debug("Connection to PostgreSQL DB closed")

    @connection_required
    def _execute_query(self, query: str, params: Optional[tuple] = None) -> RealDictCursor:
        cursor = self.__connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            self.__logger.debug(f"Executing query: {query}, params: {params}")
            cursor.execute(query, params)
            self.__connection.commit()
            self.__logger.debug("Query executed successfully")
            return cursor
        except Exception as e:
            self.__logger.error(f"Error during execute query: '{e}'")
            raise e

    @connection_required
    def _fetch_query(self, query: str, params: Optional[tuple] = None) -> list[dict]:
        cursor = self.__connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            self.__logger.debug(f"Executing query: {query}, params: {params}")
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            self.__logger.error(f"Error during fetch query: '{e}'")
            raise e

    def __add_criteria_to_query(
        self, *, query: str, criteria: list[SqlCriteria]
    ) -> tuple[str, list[any]]:
        query_conditions = []
        params = []
        for criterion in criteria:
            match criterion.sql_operator:
                case SqlOperator.EQUAL | SqlOperator.NOT_EQUAL | SqlOperator.LESS_THAN | SqlOperator.LESS_THAN_OR_EQUAL | SqlOperator.GREATER_THAN | SqlOperator.GREATER_THAN_OR_EQUAL | SqlOperator.LIKE | SqlOperator.NOT_LIKE:
                    query_conditions.append(
                        f"{criterion.column_name} {criterion.sql_operator.value} %s"
                    )
                    params.append(criterion.value)
                case SqlOperator.IN:
                    if not isinstance(criterion.value, list) and not isinstance(
                        criterion.value, set
                    ):
                        raise SqlException(
                            f"Trying to use '{SqlOperator.IN.value}' with non-iterable '{criterion.value}'"
                        )
                    query_conditions.append(
                        f"{criterion.column_name} {criterion.sql_operator.value} ({', '.join(['%s'] * len(criterion.value))})"
                    )
                    params += criterion.value
                case _:
                    raise NotImplementedError(
                        f"SQL Operator: {criterion.sql_operator.name} has not been implemented."
                    )

        query += " WHERE " + " AND ".join(query_conditions)
        return query, params

    def __add_order_bys_to_query(self, *, query: str, order_bys: list[SqlOrderBy]) -> str:
        order_by_queries = []
        for order_by in order_bys:
            sort_direction = (
                "" if order_by.sort_direction is None else order_by.sort_direction.value
            )
            order_by_queries.append(f" ORDER BY {order_by.expression} {sort_direction}")
        query += ", ".join(order_by_queries)
        return query

    @connection_required
    def _get_rows(
        self,
        *,
        schema: str,
        table: str,
        obj_class: Optional[DictDeserializable] = None,
        selections: Optional[list[str]] = None,
        criteria: Optional[list[SqlCriteria]] = None,
        group_by: Optional[str] = None,
        order_bys: Optional[list[SqlOrderBy]] = None,
        limit: Optional[int] = None,
    ) -> list[DictDeserializable]:
        selection = "*" if selections is None else ", ".join(selections)
        query = f"SELECT {selection} FROM {schema}.{table}"
        params = []

        if criteria:
            query, params = self.__add_criteria_to_query(query=query, criteria=criteria)

        if group_by is not None:
            query += f" GROUP BY {group_by}"

        if order_bys is not None:
            query = self.__add_order_bys_to_query(query=query, order_bys=order_bys)

        if limit is not None:
            query += " LIMIT %s"
            params.append(limit)

        self.__logger.debug(f"Executing query: {query}, params: {params}")
        all_rows = self._fetch_query(query, tuple(params))

        if obj_class is not None:
            all_rows = [obj_class.from_dict(row) for row in all_rows]

        return all_rows

    @connection_required
    def _get_count(
        self, *, schema: str, table: str, criteria: Optional[list[SqlCriteria]] = None
    ) -> int:
        query = f"SELECT COUNT(*) FROM {schema}.{table}"
        params = []

        if criteria:
            query, params = self.__add_criteria_to_query(query=query, criteria=criteria)

        self.__logger.debug(f"Executing query: {query}, params: {params}")
        all_rows = self._fetch_query(query, tuple(params))

        if len(all_rows) == 0:
            return 0
        return all_rows[0]["count"]
