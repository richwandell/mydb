from typing import List

from src.language import SQLiteLexer, SQLiteParser, SQLiteParserListener
from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker


class Column:
    name: str

    def __init__(self, col_name: str):
        self.name = col_name


class Statement:
    pass


class Table(Statement):
    name: str

    def __init__(self, table_name: str):
        self.name = table_name


class Where:
    pass


class SelectStatement(Statement):
    select_clause: List[Column]
    from_clause: List[Statement]
    where_clause: List[Where]

    def __init__(self, columns: List[Column], from_clause: List[Statement], where_clause: List[Where]):
        self.where_clause = where_clause
        self.from_clause = from_clause
        self.columns = columns


class Listener(SQLiteParserListener):

    statements: List[SelectStatement]

    def __init__(self):
        self.statements = []

    def enterSelect_stmt(self, ctx:SQLiteParser.Select_stmtContext):
        for sel_cor_ctx in ctx.children:
            columns = []
            tables = []
            for child in sel_cor_ctx.children:
                if type(child) == SQLiteParser.Result_columnContext:
                    child: SQLiteParser.Result_columnContext

                    star = child.STAR()
                    if star is not None:
                        columns.append(Column("*"))
                        continue

                    ex = child.expr()
                    if ex is not None:
                        col = ex.column_name()
                        if col is not None:
                            col_name = col.any_name()
                            if col_name is not None:
                                col_name = col_name.IDENTIFIER()
                                columns.append(Column(str(col_name)))
                if type(child) == SQLiteParser.Table_or_subqueryContext:
                    child: SQLiteParser.Table_or_subqueryContext
                    table_name = str(child.table_name().any_name().IDENTIFIER())
                    tables.append(Table(table_name))
            self.statements.append(SelectStatement(columns, tables, []))


def create_statements(sql: str):
    input_stream = InputStream(sql)
    lexer = SQLiteLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SQLiteParser(stream)
    tree = parser.parse()
    printer = Listener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    return printer.statements


if __name__ == '__main__':

    statements = create_statements("select instruction from nestest_log")


    print(statements)