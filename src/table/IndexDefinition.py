from typing import List

from src.table import ColumnDefinition


class IndexDefinition:
    name: str
    columns: List[ColumnDefinition]

    def __init__(self, name: str, columns: List[ColumnDefinition]):
        self.name = name
        self.columns = columns

    @staticmethod
    def from_dict(index, columns):
        ic = []
        for col_name in index["columns"]:
            ic.append(next(x for x in columns if x.column_name == col_name))
        return IndexDefinition(index["name"], ic)

    @staticmethod
    def to_dict(index):
        return {
            "name": index.name,
            "columns": list(c.column_name for c in index.columns)
        }
