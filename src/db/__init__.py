from __future__ import annotations

import json
import os
from typing import Dict

from src import Config
from src.table import TableDefinition, Column


class Db:

    config: Config
    table_definitions: Dict[str, TableDefinition]

    def __init__(self, config: Config):
        self.config = config
        os.makedirs(config.data_folder, exist_ok=True)
        self.table_definitions = self.load_table_definitions()

    def load_table_definitions(self):
        tdf = self.config.data_folder + "/table_definitions.json"
        try:
            with open(tdf) as defs_file:
                tables = json.loads(defs_file.read())
                all_tables = {}
                for table in tables:
                    columns = list(Column.from_dict(c) for c in table["columns"])
                    all_tables[table["table_name"]] = TableDefinition(table["table_name"], columns)
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

    def create_table(self, table_definition: TableDefinition):

        pass





