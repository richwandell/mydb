from typing import List

from src.table import ColumnDefinition, IndexDefinition


class TableDefinition:
    name: str
    columns: List[ColumnDefinition]
    indexes: List[IndexDefinition]
    row_size: int

    def __init__(self, name: str, columns: List[ColumnDefinition], indexes: List[IndexDefinition]):
        self.name = name
        self.columns = columns
        self.indexes = indexes
        self.row_size = sum(column.max_length for column in self.columns)

    def to_dict(self):
        return {
            "table_name": self.name,
            "columns": list(ColumnDefinition.to_dict(c) for c in self.columns),
            "indexes": list(IndexDefinition.to_dict(i) for i in self.indexes)
        }
