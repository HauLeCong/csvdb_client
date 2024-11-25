
import pytest
from collections.abc import Iterator
from typing import Tuple, List

from dbcsv_server.query_engine.parser import Parser
from dbcsv_server.query_engine.parser.predicate_parser import PredicateParser
from dbcsv_server.query_engine.ast_node import (
    ColumnNode, 
    ColumnListNode, 
    SelectNode, 
    FromNode, 
    ExprNode, 
    PredicateNode,
    PredicateOrNode,
    PredicateAndNode,
    PredicateNotNode,
    PredicateCompareNode,
    
) 
from dbcsv_server.query_engine.token import Token
from dbcsv_server.query_engine.planner.handler.expression_handler import ExpressionHandler
from dbcsv_server.query_engine.planner.handler.column_list_handler import ColumnListHandler
from dbcsv_server.query_engine.planner.handler.predicate_handler import PredicateHandler
from dbcsv_server.query_engine.planner.handler.create_table_handler import CreateTableHandler
from dbcsv_server.query_engine.parser.expression_parser import ExpressionParser
from dbcsv_server.query_engine.printer import ASTPrinter

def print_tree(node):
        level = 0
        def print_node(obj, lvl) -> int:
            if not hasattr(obj, "left"):
                if hasattr(obj.expr, "left"):
                    if obj.expr.right:
                        lvl += 1
                        print(f"level {lvl}:{obj.expr.left.__class__.__name__}{obj.expr.operator.value}{obj.expr.right.__class__.__name__}")
                        print_node(obj.expr.left, lvl)
                        print_node(obj.expr.right, lvl)
                    else:
                        lvl += 1
                        print(f"level {lvl}:{obj.left.__class__.__name__}")
                        print_node(obj.expr.left, lvl)
                else:
                    print(f"level {lvl}:{obj.expr}")
            elif hasattr(obj, "left"):
                if obj.right:
                    lvl += 1
                    print(f"level {lvl}:{obj.left.__class__.__name__}{obj.operator.value}{obj.right.__class__.__name__}")
                    print_node(obj.left, lvl)
                    print_node(obj.right, lvl)
                else:
                    lvl += 1
                    print(f"level {lvl}:{obj.left.__class__.__name__}")
                    print_node(obj.left, lvl)
        print_node(node, level)

@pytest.mark.parametrize("valid_number", ["1.23", ".123", "123"])
def test_scan_number_return_valid_number(valid_number):
    """
        Test parser.sacn_number return valide number
    """
    parser = Parser(valid_number)
    assert parser.scan_number() == valid_number
    
@pytest.mark.parametrize("invalid_number", ["1.234a", " .j123", "123.a"])
def test_scan_number_return_invalid_number(invalid_number):
    """
        Test parser scan number return invalid error
    """
    parser = Parser(invalid_number)
    with pytest.raises(ValueError) as e:
       assert parser.scan()
   
@pytest.mark.parametrize("valid_string, expected", [("abc\r\n", "abc"), ("_abc\r\n", "_abc"), ("\"abc def\"\r\n", "abc def")])
def test_valid_string(valid_string, expected):
    """
    Test parser return valid string on scan
    """
    parser = Parser(valid_string)
    assert parser.scan_string() == expected.upper()

@pytest.mark.parametrize("invalid_string", ["\"abc"])
def test_not_closed_string(invalid_string):
    """
    Test return error when string not closed
    """
    parser = Parser(invalid_string)
    with pytest.raises(ValueError) as e:
        assert parser.scan_string()
    
    assert e.value.args[0] == f"Invalid token string was not closed"
    
@pytest.mark.parametrize("valid_query", [
    "select * from table", 
    "select abc as a from table", 
    """select "abc" as "a" from table """
    ]
)
def test_parse_column(valid_query):
    parser = Parser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    column_node = parser.parse_column()
    assert isinstance(column_node, ColumnNode)
    
# @pytest.mark.parametrize("valid_query", [
#         # "select a, b, c as c1 from table",
#         "select 1 + 2 + 3, a, c from table"
#     ]
# )
# def test_parse_column_list(valid_query):
#     parser = Parser(valid_query)
#     parser.scan()
#     parser.iter_token = iter(parser.token)
#     parser.advance_token()
#     parser.advance_token()
#     print(parser.current_token)
#     column_list_node = parser.parse_column_list()
    # print(parser.token)
    # print(column_list_node)
    # print_tree(column_list_node)
    # assert isinstance(column_list_node, ColumnListNode)

    
@pytest.mark.parametrize("select_query", [
    "select a, b, c, 1+2+3 from xyz.abc \r\n"
])
def test_parse_select(select_query):
    parser = Parser(select_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    print(parser.token)
    select_clause = parser.parse_select_clause()
    print(select_clause)
    assert isinstance(select_clause, SelectNode)

    
# @pytest.mark.parametrize("valid_query", ["select a, b, 1+2+3 from xyz"])
# def test_return_select_node_value(valid_query):
#     parser = Parser(valid_query)
#     parser.scan()
#     parser.iter_token = iter(parser.token)
#     parser.advance_token()
#     parser.advance_token()
#     select_node = parser.parse_select_clause()
#     print(select_node)
#     planner = QueryPlanner()
#     select = planner.visit(select_node)
#     print(select)
#     assert isinstance(select_node, SelectNode)    

    
@pytest.mark.parametrize("valid_query", ["select a from xyz", "select 1+2*3 from xyz", "select a*2+10 from xyz"])
def test_parse_expr(valid_query):
    parser = Parser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    expr_node = parser.parse_expr()
    assert isinstance(expr_node, ExprNode)
    
@pytest.mark.parametrize("valid_query", ["select a from xyz", "select 1+2*3 from xyz", "select a*2+10 from xyz"])
def test_print_expr_node(valid_query):
    parser = Parser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    expr_node = parser.parse_expr()
    assert isinstance(expr_node, ExprNode)
    printer = ASTPrinter()
    printer.print_node(expr_node, 0)
    
@pytest.mark.parametrize("valid_query", ["select a from xyz", "select a+1+2*4", """select a as "A" """])
def test_print_column_node(valid_query):
    parser = Parser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    print(parser.token)
    column_node = parser.parse_column()
    assert isinstance(column_node, ColumnNode)
    printer = ASTPrinter()
    printer.print_node(column_node, 0)
    
@pytest.mark.parametrize("valid_query", ["select a, b, c from xyz", "select 1 as a from abc", "select a, 1*4+5, c from xyz"])
def test_print_column_list_node(valid_query):
    parser = Parser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    print(parser.token)
    column_list_node = parser.parse_column_list()
    assert isinstance(column_list_node, ColumnListNode)
    print(column_list_node)
    printer = ASTPrinter()
    printer.print_node(column_list_node, 0)
    
@pytest.mark.parametrize("valid_query", ["1 > a", "a = b", "c >= d", "d <= e", "1 > 2", "3<>4"])
def test_parse_predicate_compare(valid_query):
    parser = Parser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    predicate_parser = PredicateParser(parser)
    predicate_compare = predicate_parser._parse_predicate_compare_node()
    assert isinstance(predicate_compare, PredicateCompareNode)
    ast_printer = ASTPrinter()
    ast_printer.print_node(predicate_compare, 0)
    
@pytest.mark.parametrize("valid_query", ["NOT A = B", "NOT 1 = 2", "NOT 1 <> 3", "NOT (1>2)"])
def test_parse_predicate_not(valid_query, ast_printer):
    parser = Parser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    print(parser.token)
    predicate_parser = PredicateParser(parser)
    predicate_not = predicate_parser._parse_predicate_not_node()
    assert isinstance(predicate_not, PredicateNotNode)
    ast_printer.print_node(predicate_not)
    

@pytest.mark.parametrize("valid_query", ["A=b AND D=e", "1*3+2 = 4 AND NOT(4>5 AND 1=2)"])
def test_parse_predicate_and(valid_query):
    parser = Parser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    print(parser.token)
    parser.advance_token()
    predicate_parser = PredicateParser(parser)
    predicate_and = predicate_parser._parse_predicate_and_node()
    assert isinstance(predicate_and, PredicateAndNode)
    print(predicate_and)
    printer = ASTPrinter()
    printer.print_node(predicate_and, 0)
    
@pytest.mark.parametrize("valid_query", ["1 + 2 = 3 OR a > 1", " a > b OR c > d", "a = b AND c=d OR e = f"])
def test_parse_predicate_or(valid_query):
    parser = Parser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    predicate_parser = PredicateParser(parser)
    predicate_or = predicate_parser._parse_predicate_or_node()
    assert isinstance(predicate_or, PredicateOrNode)
    print(predicate_or)
    printer = ASTPrinter()
    printer.print_node(predicate_or, 0)
    
    
@pytest.mark.parametrize("valid_query", ["select * from abc", "select * from abc.xyz.dfa"])
def test_parse_token_from(valid_query):
    parser = Parser(valid_query)
    parser.scan()
    print(parser.token)
        
    
@pytest.mark.parametrize("valid_query", ["select a+1-2*4"])
def test_hanle_expression_add_node(valid_query, caller):
    parser = Parser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    expression_parser = ExpressionParser(parser)
    add_node = expression_parser._parse_expr_add()
    printer = ASTPrinter()
    printer.print_node(add_node)
    planner = ExpressionHandler(caller)
    result = planner.handle_expression_add_node(add_node)
    assert result == 1+1-2*4
   
@pytest.mark.parametrize("valid_query", ["select a+1-2*4"]) 
def test_handle_column_node(valid_query, caller):
    parser = Parser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    column_node = parser.parse_column()
    printer = ASTPrinter()
    print(column_node.name)
    printer.print_node(column_node)
    planner = ColumnListHandler(caller)
    result = planner.handle_column_node(column_node)
    assert result == {f"{column_node.name}": 1+1-2*4}
    
@pytest.mark.parametrize("valid_query", ["select a+1-2*4, a, a as c2 from xyz"]) 
def test_handle_column_node(valid_query, caller):
    parser = Parser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    column_list_node = parser.parse_column_list()
    printer = ASTPrinter()
    printer.print_node(column_list_node)
    planner = ColumnListHandler(caller)
    result = planner.handle(column_list_node)
    print("***Result****", result)
    assert result == {'columns': ('A + 1.0 - 2.0 * 4.0', 'A', 'C2'), 'data': (-6.0, 1, 1)}
    
@pytest.mark.parametrize("valid_query", ["1=2 OR 3=4"])
def test_handle_predicate_node(valid_query, caller):
    parser = Parser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    predicate_parser = PredicateParser(parser)
    predicate_or_node = predicate_parser._parse_predicate_or_node() 
    print(predicate_or_node)
    printer = ASTPrinter()
    printer.print_node(predicate_or_node)
    handler = PredicateHandler(caller)
    result = handler.handle_predicate_or_node(predicate_or_node)
    assert result == False
    
    
@pytest.mark.parametrize("valid_query", [
    "select * from abc.def \r\n", 
    "select 1+2*3, a as c from abc.def \r\n", 
    "select a from b.c where a=b \r\n", 
    "select a from v.z \r\n"])
def test_print_select_node(valid_query):
    parser = Parser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    print(parser.token)
    select_node = parser.parse_select_clause()
    print(select_node)
    printer = ASTPrinter()
    printer.print_node(select_node)

@pytest.mark.parametrize("valid_query",[
    "select * from abc.def \r\n", 
    "select 1+2*3, a as c from abc.def \r\n", 
    "select a from b.c where a=b \r\n", 
    "select a from v.z \r\n"
    ])
def test_parse_full_ast(valid_query):
    parser = Parser(valid_query)
    parser.scan()
    print(parser.token)
    ast = parser.parse()
    print(ast.nodes)
    printer = ASTPrinter()
    printer.print_node(ast)
    
from dbcsv_server.query_engine.parser.create_table_parser import CreateTableParser
    
@pytest.mark.parametrize("valid_query", ["CREATE TABLE t.data (a INT, b FLOAT, c FLOAT)"])
def test_create_table_parse(valid_query):
    parser = Parser(valid_query)
    parser.scan()
    # print(parser.token)
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    parser.advance_token()
    print(parser.current_token)
    create_table_parser = CreateTableParser(parser)
    create_table_node = create_table_parser.parse()
    print(create_table_node)
    
@pytest.mark.parametrize("valid_query", ["CREATE TABLE a.t (a INT, b FLOAT)"])  
def test_create_table_handler(valid_query, caller):
    parser = Parser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    ast = parser.parse()
    create_table_handler = CreateTableHandler(caller)
    result = create_table_handler.handle(ast.nodes)
    print("***", result)


from dbcsv_server.query_engine.planner.table_creation import TableCreation
    
@pytest.mark.parametrize("valid_query", ["CREATE TABLE a.t (a STRING, b STRING)"])
def test_creation_table(valid_query, caller):
    parser = Parser(valid_query)
    ast_node = parser.parse()
    table_creation = TableCreation(ast_node.nodes)
    assert table_creation._get_create_column_list() == [{"column_name": "A", "column_type": "STRING"},{"column_name": "B", "column_type": "STRING"}]


from dbcsv_server.connection import ConnectionIdentity
from dbcsv_server.data_storage import FileManager
from dbcsv_server.query_engine.planner.production import Production
from dbcsv_server.query_engine.planner.projection import Projection
from dbcsv_server.query_engine.planner.selection import Selection
from pathlib import Path

@pytest.mark.parametrize("valid_query", ["SELECT col3 + 2 * 3 AS E FROM A.T WHERE col3 = 1\r\n"])
def test_all_relational_operator(valid_query):
    con = ConnectionIdentity(Path("data/storage"))
    file_manager = FileManager()
    parser = Parser("CREATE TABLE A.T (col1 STRING, col2 STRING, col3 FLOAT)")
    ast_nodes = parser.parse()
    table_creation = TableCreation(ast_nodes.nodes)
    database = table_creation._get_create_database()
    columns_definition = table_creation._get_create_column_list()
    table_name = table_creation._get_create_table_name()
    assert table_name == "T"
    assert columns_definition == [{"column_name": "COL1", "column_type": "STRING"}, {"column_name": "COL2", "column_type": "STRING"}, {"column_name": "COL3", "column_type":"FLOAT"}]
    result_file = file_manager.create_table_file(con, database, table_name, columns_definition)
    assert result_file.exists()
    
    #Insert mock data
    with open(f"data/storage/{database}/{table_name}.csv", "a") as r:
        r.write("A, B, 1")
        
    data_select = file_manager.select_file(con, database, table_name)
    print(data_select)
    assert data_select == [{'COL1': 'A', 'COL2': ' B', 'COL3': 1}]
    
    parser = Parser(valid_query)
    ast_nodes = parser.parse()
    from functools import partial
    production = Production(ast_nodes.nodes.from_clause, partial(file_manager.select_file, con = con))
    assert production.source == [{'COL1': 'A', 'COL2': ' B', 'COL3': 1}]
    
    selection = Selection(node = ast_nodes.nodes.where_clause.expr,source= production)
    
    projection = Projection(ast_nodes.nodes.column_list, selection)
    row_result = next(projection)
    print("****", row_result)
    assert row_result == {'columns': ('E', ), 'data': (7, )}
