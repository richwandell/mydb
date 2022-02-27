import enum
from typing import List


class ColumnType(enum.Enum):
    string = 0
    integer = 1


class ColumnDefinition:
    column_name: str
    column_type: ColumnType
    max_length: int

    def __init__(self, column_name: str, column_type: ColumnType, max_length: int):
        self.column_name = column_name
        self.max_length = max_length
        self.column_type = column_type

    @staticmethod
    def from_dict(column: dict):
        assert "column_name" in column and "column_type" in column and "max_length" in column
        return ColumnDefinition(column["column_name"], ColumnType(column["column_type"]), column["max_length"])

    def to_dict(self):
        return {
            "column_name": self.column_name,
            "column_type": self.column_type.value,
            "max_length": self.max_length
        }


class IndexDefinition:
    name: str
    columns: List[ColumnDefinition]

    def __init__(self, name: str, columns: List[ColumnDefinition]):
        self.name = name
        self.columns = columns

    @staticmethod
    def from_dict(index, columns):
        ic = list(filter(lambda x: x.column_name in index["columns"], columns))
        return IndexDefinition(index["name"], ic)

    @staticmethod
    def to_dict(index):
        return {
            "name": index.name,
            "columns": list(c.column_name for c in index.columns)
        }


class TableDefinition:
    name: str
    columns: List[ColumnDefinition]
    indexes: List[IndexDefinition]

    def __init__(self, name: str, columns: List[ColumnDefinition], indexes: List[IndexDefinition]):
        self.name = name
        self.columns = columns
        self.indexes = indexes

    def to_dict(self):
        return {
            "table_name": self.name,
            "columns": list(ColumnDefinition.to_dict(c) for c in self.columns),
            "indexes": list(IndexDefinition.to_dict(i) for i in self.indexes)
        }



