from __future__ import annotations

import binascii
import json
from typing import Any, List, Dict

from .exceptions import TableDoesNotExist
from src.table import ColumnDefinition, ColumnType, TableDefinition, IndexDefinition


def table_exists(func):
    def inner(*args, **kwargs):
        if args[1] not in args[0].table_definitions:
            raise TableDoesNotExist
        return func(*args, **kwargs)
    return inner


def convert_column(column: ColumnDefinition, data: Any):
    if column.column_type == ColumnType.integer:
        return int.from_bytes(data, "big")
    else:
        return data.decode("utf8")


def convert_row(raw_row, t_def: TableDefinition) -> List[str | int]:
    row = []
    offset = 0
    for column in t_def.columns:
        size = int.from_bytes(raw_row[offset:offset+4], "big")
        data = raw_row[offset+4:offset + 4 + size]
        row.append(convert_column(column, data))
        offset += 4 + column.max_length
    return row


def str_to_int(s: str) -> int:
    return int(binascii.hexlify(s.encode("utf8")), 16)


def load_table_definitions(data_folder) -> Dict[str, TableDefinition]:
    tdf = data_folder + "/table_definitions.json"
    try:
        with open(tdf) as defs_file:
            tables = json.loads(defs_file.read())
            all_tables = {}
            for table in tables:
                columns = list(ColumnDefinition.from_dict(c) for c in table["columns"])
                indexes = list(IndexDefinition.from_dict(i, columns) for i in table["indexes"])
                all_tables[table["table_name"]] = TableDefinition(table["table_name"], columns, indexes)
            return all_tables
    except FileNotFoundError as e:
        with open(tdf, "w+") as defs_file:
            defs_file.write(json.dumps([]))
            return {}
