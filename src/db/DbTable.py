import hashlib
import os

from src import Config
from src.table import TableDefinition


class DbTable:

    def __init__(self, table_definition: TableDefinition, config: Config):
        tnh = hashlib.md5(table_definition.name.encode("utf8")).hexdigest()
        file_path = config.data_folder + "/data." + tnh
        file_size = os.path.getsize('d:/file.jpg')
        try:
            with open(file_path, "rb") as file:
                self.b_tree = pickle.load(file)
        except FileNotFoundError:
            self.b_tree = BTree(5)
            with open(file_path, "wb+") as file:
                pickle.dump(self.b_tree, file)
        except Exception as e:
            print(e)