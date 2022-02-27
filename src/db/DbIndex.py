import hashlib
import pickle

from src import Config
from src.index import BTree
from src.table import TableDefinition, IndexDefinition


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
