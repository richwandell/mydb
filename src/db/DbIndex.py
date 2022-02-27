import datetime
import hashlib
import pickle
import binascii
from typing import Any

from src import Config
from src.index import BTree
from src.table import TableDefinition, IndexDefinition


def convert_key(key: Any):
    if type(key) == bytes:
        return int(binascii.hexlify(key), 16)
    elif type(key) == str:
        return int(binascii.hexlify(key.encode("utf8")), 16)
    elif type(key) == int:
        return key


class DbIndex:

    b_tree: BTree
    file_path: str
    index_definition: IndexDefinition
    last_saved: datetime.datetime
    updated: bool

    def __init__(self, table_definition: TableDefinition, index_definition: IndexDefinition, config: Config):
        self.index_definition = index_definition
        tnh = hashlib.md5(table_definition.name.encode("utf8")).hexdigest()
        idh = hashlib.md5(self.index_definition.name.encode("utf8")).hexdigest()
        self.file_path = config.data_folder + "/index." + tnh + "." + idh
        try:
            with open(self.file_path, "rb") as file:
                self.b_tree = pickle.load(file)
        except FileNotFoundError:
            self.reset()
        except Exception as e:
            print(e)
        self.last_saved = datetime.datetime.now()
        self.updated = False

    def get(self, key):
        key = convert_key(key)
        node = self.b_tree.find_insertion(self.b_tree.root, key)
        if node.is_leaf:
            return node.data
        return []

    def insert(self, key: Any, data: Any, save=False):
        self.updated = True
        key = convert_key(key)
        self.b_tree.insert(key, data)
        if save:
            self.save()

    def save(self):
        with open(self.file_path, "wb+") as file:
            pickle.dump(self.b_tree, file)
        self.last_saved = datetime.datetime.now()
        self.updated = False

    def reset(self):
        self.b_tree = BTree(5)
        self.save()
