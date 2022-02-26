import enum
from typing import List


class ColumnType(enum.Enum):
    string = 0
    integer = 1


class Column:
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
        return Column(column["column_name"], ColumnType(column["column_type"]), column["max_length"])

    def to_dict(self):
        return {
            "column_name": self.column_name,
            "column_type": self.column_type.value,
            "max_length": self.max_length
        }


class TableDefinition:
    name: str
    columns: List[Column]

    def __init__(self, name: str, columns: List[Column]):
        self.name = name
        self.columns = columns

    def to_dict(self):
        return {
            "table_name": self.name,
            "columns": list(Column.to_dict(c) for c in self.columns)
        }
