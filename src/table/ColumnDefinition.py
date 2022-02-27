from src.table import ColumnType


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