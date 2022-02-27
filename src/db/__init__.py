from __future__ import annotations

import json
import os
import pickle
import hashlib
from typing import Dict, List, Any

from src import Config
from src.index import BTree
from src.table import TableDefinition, ColumnDefinition, IndexDefinition


class DbIndex:

    b_tree: BTree

    def __init__(self, table_definition: TableDefinition, index_definition: IndexDefinition, config: Config):
        tnh = hashlib.md5(table_definition.name.encode("utf8")).hexdigest()
        idh = hashlib.md5(index_definition.name.encode("utf8")).hexdigest()
        file_path = config.data_folder + "/index." + tnh + "." + idh
        try:
            with open(file_path, "rb") as file:
                self.b_tree = pickle.load(file)
        except FileNotFoundError:
            self.b_tree = BTree(5)
            with open(file_path, "wb+") as file:
                pickle.dump(self.b_tree, file)
        except Exception as e:
            print(e)


class Db:

    config: Config
    table_definitions: Dict[str, TableDefinition]
    indexes: Dict[str, DbIndex]

    def __init__(self, config: Config):
        self.config = config
        os.makedirs(config.data_folder, exist_ok=True)
        self.table_definitions = self.load_table_definitions()
        self.indexes = self.load_indexes()

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

        pass

    def create_table(self, table_definition: TableDefinition):

        pass





