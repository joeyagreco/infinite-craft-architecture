from typing import Any

from model.abstract.DictSerializable import DictSerializable


class BaseSqlRepository:
    def __init__(self, *, schema: str, table: str, primary_key: str):
        self._schema = schema
        self._table = table
        self._primary_key = primary_key

    def _build_insert_query(
        self, *, rows: list[DictSerializable], do_nothing_on_conflict: bool = False
    ) -> tuple[str, list[Any]]:
        """
        Builds a query to insert the given rows.
        Returns the query and the params for the query.
        """
        rows_dict = [row.to_dict() for row in rows]
        columns = ", ".join(column for column in rows_dict[0].keys())
        placeholders = ", ".join("%s" for _ in rows_dict[0].values())
        values = ", ".join(f"({placeholders})" for _ in rows_dict)
        conflict_clause = ""

        if do_nothing_on_conflict:
            conflict_clause = f" ON CONFLICT DO NOTHING"

        query = f"INSERT INTO {self._schema}.{self._table} ({columns}) VALUES {values}{conflict_clause};"
        params = [value for row in rows_dict for value in row.values()]
        return query, params

    def _build_update_query(self, row: DictSerializable) -> tuple[str, list[Any]]:
        """
        Builds a query to update a row based on the primary key.
        Returns the query and the params for the query.
        """
        row_dict = row.to_dict()
        set_columns = ", ".join(
            f"{key} = %s" for key in row_dict.keys() if key != self._primary_key
        )
        condition_column = f"{self._primary_key} = %s"

        query = f"UPDATE {self._schema}.{self._table} SET {set_columns} WHERE {condition_column};"
        params = [value for key, value in row_dict.items() if key != self._primary_key]
        params.append(row_dict[self._primary_key])
        return query, params

    def _build_delete_query(self, column_name: str, value: Any) -> tuple[str, list[Any]]:
        """
        Builds a query to delete a row based on the column name and value.
        Returns the query and the params for the query.
        """
        query = f"DELETE FROM {self._schema}.{self._table} WHERE {column_name} = %s;"
        params = [value]
        return query, params
