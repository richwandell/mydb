from __future__ import annotations

import json
import os
from typing import Dict, List, Any

from src import Config
from src.table import TableDefinition, ColumnType
from .DbIndex import DbIndex
from .TableMeta import TableMeta
from .functions import load_table_definitions, str_to_int, convert_row, convert_column, table_exists
from ..language.functions import create_statements, SelectStatement


class Db:

    config: Config
    table_definitions: Dict[str, TableDefinition]
    table_meta: Dict[str, TableMeta]
    indexes: Dict[str, Dict[str, List[DbIndex]]]

    def __init__(self, config: Config):
        self.config = config
        os.makedirs(config.data_folder, exist_ok=True)
        self.table_definitions = load_table_definitions(config.data_folder)
        self.indexes = self.load_indexes()
        self.table_meta = self.load_table_meta()

    def load_table_meta(self) -> Dict[str, TableMeta]:
        meta = {}
        for key in self.table_definitions.keys():
            t_def = self.table_definitions[key]
            meta[t_def.name] = TableMeta(t_def, self.config)
        return meta

    def load_indexes(self) -> Dict[str, Dict[str, List[DbIndex]]]:
        indexes = {}
        for key in self.table_definitions.keys():
            tdef = self.table_definitions[key]
            indexes[tdef.name] = {}
            for index_definition in tdef.indexes:
                index = DbIndex(tdef, index_definition, self.config)
                for col in index_definition.columns:
                    if col.column_name not in indexes[tdef.name]:
                        indexes[tdef.name][col.column_name] = []
                    indexes[tdef.name][col.column_name].append(index)
        return indexes

    def save_table_definitions(self):
        with open(self.config.data_folder + "/table_definitions.json", "w") as defs_file:
            all_tables = []
            for table in self.table_definitions.keys():
                table_def = self.table_definitions[table]
                all_tables.append(table_def.to_dict())
            defs_file.write(json.dumps(all_tables))

    @table_exists
    def insert(self, table: str, data: List[Any]):
        t_def = self.table_definitions[table]
        t_meta = self.table_meta[table]
        row = bytearray(t_def.row_size)
        offset = 0
        table_indexes = self.indexes[table]
        for i, column in enumerate(t_def.columns):
            if column.column_type == ColumnType.string:
                if type(data[i]) == int:
                    data[i] = str(data[i])
                cb = bytes(data[i].encode("utf8"))
                actual_size = len(cb).to_bytes(4, 'big')
            else:
                if type(data[i]) == str:
                    data[i] = str_to_int(data[i])
                cb = data[i].to_bytes(column.max_length, 'big')
                actual_size = column.max_length.to_bytes(4, 'big')
            row[offset:offset+4] = actual_size
            row[offset+4:offset+4+len(cb)] = cb
            offset += 4 + column.max_length
            if column.column_name in table_indexes.keys():
                for index in table_indexes[column.column_name]:
                    index.insert(cb, t_meta.file_size)

        with open(t_meta.file_path, 'ab') as file:
            file.write(row[0:t_def.row_size])
            t_meta.file_size += t_def.row_size

    @table_exists
    def find_row(self, table: str, column: str, search: Any, use_index=True):
        def cmp(index):
            return -1 if index.index_definition.columns[0].column_name == column else 1

        t_meta = self.table_meta[table]
        t_def = self.table_definitions[table]
        table_indexes = self.indexes[table]
        return_rows = []
        if use_index and column in table_indexes:
            usable_indexes = sorted(table_indexes[column], key=cmp)
            index = usable_indexes[0]
            row_positions = index.get(search)
            with open(t_meta.file_path, 'rb') as file:
                for offset in row_positions:
                    file.seek(offset)
                    return_rows.append(convert_row(file.read(t_def.row_size), t_def))
        else:
            column_offset = 0
            column_size = 0
            column_definition = None
            for col in t_def.columns:
                if col.column_name == column:
                    column_definition = col
                    column_size = col.max_length + 4
                    break
                column_offset += col.max_length + 4
            with open(t_meta.file_path, 'rb') as file:
                row_offset = 0
                while row_offset < t_meta.file_size:
                    file.seek(row_offset + column_offset)
                    data = file.read(column_size)
                    size = int.from_bytes(data[0:4], "big")
                    test_col = convert_column(column_definition, data[4:4+size])
                    if test_col.find(search, 0, len(search)) == 0:
                        file.seek(row_offset)
                        return_rows.append(convert_row(file.read(t_def.row_size), t_def))
                    row_offset += t_def.row_size
        return return_rows

    @table_exists
    def get_rows(self, table: str, row_nums: List[int]):
        t_meta = self.table_meta[table]
        t_def = self.table_definitions[table]
        return_rows = []
        with open(t_meta.file_path, 'rb') as file:
            for row_num in row_nums:
                offset = row_num * t_def.row_size
                file.seek(offset)
                return_rows.append(convert_row(file.read(t_def.row_size), t_def))
        return return_rows

    @table_exists
    def _get_row(self, table: str, row_num: int) -> bytes:
        t_def = self.table_definitions[table]
        t_meta = self.table_meta[table]
        with open(t_meta.file_path, 'rb') as file:
            offset = row_num * t_def.row_size
            file.seek(offset)
            return file.read(t_def.row_size)

    @table_exists
    def get_row(self, table: str, row_num: int):
        t_def = self.table_definitions[table]
        raw_row = self._get_row(table, row_num)
        return convert_row(raw_row, t_def)

    @table_exists
    def truncate_table(self, table: str):
        t_meta = self.table_meta[table]
        with open(t_meta.file_path, 'w') as file:
            pass
        t_meta.file_size = 0
        if table in self.indexes:
            for col_key in self.indexes[table].keys():
                col_indexes = self.indexes[table][col_key]
                for index in col_indexes:
                    index.reset()

    def create_table(self, table_definition: TableDefinition):
        pass

    def query(self, sql: str):
        statements = create_statements(sql)
        for statement in statements:
            if type(statement) == SelectStatement:
                pass
        print(statements)