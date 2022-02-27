from typing import List

import sqlparse

from src.language import SQLiteLexer, SQLiteParser, SQLiteParserListener


class SelectStatement:

    def __init__(self):
        pass



class Listener(SQLiteParserListener):

    statement_type: str
    result_columns: List[str]
    select_statements: List[SelectStatement]

    def enterResult_column(self, ctx:SQLiteParser.Result_columnContext):
        pass

    def enterSelect_stmt(self, ctx:SQLiteParser.Select_stmtContext):
        for sel_cor_ctx in ctx.children:
            columns = sel_cor_ctx.children[1]
            table = sel_cor_ctx.children[3]
            print(columns)
        pass

    def enterSimple_select_stmt(self, ctx:SQLiteParser.Simple_select_stmtContext):
        pass

if __name__ == '__main__':
    parsed = sqlparse.parse('select * from foo')
    print(parsed)
    # import sys
    # from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
    #
    # input_stream = InputStream("select a, b from nestest_log")
    # lexer = SQLiteLexer(input_stream)
    # stream = CommonTokenStream(lexer)
    # parser = SQLiteParser(stream)
    # tree = parser.select_stmt()
    # printer = Listener()
    # walker = ParseTreeWalker()
    # walker.walk(printer, tree)

    print(tree)