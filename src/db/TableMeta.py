import hashlib
import os

from src import Config
from src.table import TableDefinition


class TableMeta:

    file_path: str
    file_size: int
    table_definition: TableDefinition

    def __init__(self, table_definition: TableDefinition, config: Config):
        self.table_definition = table_definition
        tnh = hashlib.md5(table_definition.name.encode("utf8")).hexdigest()
        self.file_path = config.data_folder + "/data." + tnh
        try:
            self.file_size = os.path.getsize(self.file_path)
        except FileNotFoundError:
            with open(self.file_path, "wb+"):
                self.file_size = 0
        except Exception as e:
            print(e)
