import json
import os
from typing import Dict, List, Any

from src import Config
from .DbIndex import DbIndex
from .TableMeta import TableMeta
from src.table import TableDefinition, ColumnDefinition, IndexDefinition


class Db:

    config: Config
    table_definitions: Dict[str, TableDefinition]
    table_meta: Dict[str, TableMeta]
    indexes: Dict[str, DbIndex]

    def __init__(self, config: Config):
        self.config = config
        os.makedirs(config.data_folder, exist_ok=True)
        self.table_definitions = self.load_table_definitions()
        self.indexes = self.load_indexes()
        self.table_meta = self.load_table_meta()

    def load_table_meta(self):
        meta = {}
        for key in self.table_definitions.keys():
            t_def = self.table_definitions[key]


    def load_indexes(self):
        indexes = {}
        for key in self.table_definitions.keys():
            tdef = self.table_definitions[key]
            for index_definition in tdef.indexes:
                index = DbIndex(tdef, index_definition, self.config)
                indexes[tdef.name] = index
        return indexes

    def load_table_definitions(self):
        tdf = self.config.data_folder + "/table_definitions.json"
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

    def save_table_definitions(self):
        with open(self.config.data_folder + "/table_definitions.json", "w") as defs_file:
            all_tables = []
            for table in self.table_definitions.keys():
                table_def = self.table_definitions[table]
                all_tables.append(table_def.to_dict())
            defs_file.write(json.dumps(all_tables))

    def insert(self, table: str, data: List[Any]):
        t_def = self.table_definitions[table]
        row = bytearray(t_def.row_size)
        offset = 0
        for i, column in enumerate(t_def.columns):
            if type(data[i]) == str:
                cb = bytes(data[i].encode("utf8"))
            else:
                cb = data[i].to_bytes(column.max_length, 'big')
            row[offset:len(cb)] = cb
            offset += column.max_length
        print(row)
        pass

    def create_table(self, table_definition: TableDefinition):

        pass