
import pytest
from collections.abc import Iterator
from typing import Tuple, List

from dbcsv_server.query_engine.parser import Parser
from dbcsv_server.query_engine.parser.predicate_parser import PredicateParser
from dbcsv_server.query_engine.ast_node import (
    ColumnNode, 
    ColumnListNode, 
    ColumnNameNode, 
    ColumnWildCardNode, 
    SelectNode, 
    FromNode, 
    WhereNode, 
    ExprNode, 
    PredicateNode,
    PredicateOrNode,
    PredicateAndNode,
    PredicateNotNode,
    PredicateCompareNode,
    PredicateParentNode,
    ExprValueNode,
    ValueNode,
    ExprParentNode
) 
from dbcsv_server.query_engine.token import Token
from dbcsv_server.query_engine.planner.handler.expression_handler import ExpressionHandler
from dbcsv_server.query_engine.planner.handler.column_list_handler import ColumnListHandler
from dbcsv_server.query_engine.parser.expression_parser import ExpressionParser
from dbcsv_server.query_engine.visitor import ASTPrinter

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
    
def test_parse_func_iter_token():
    parser = Parser("select * from test")
    parser.scan()
    parser.parse()
    assert isinstance(parser.iter_token, Iterator)

    
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
    
@pytest.mark.parametrize("from_clause", ["from abc", """from "xyz" """])
def test_parse_from_clause(from_clause):
    parser = Parser(from_clause)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    from_clause = parser.parse_from_clause()
    print(from_clause)
    assert isinstance(from_clause, FromNode)
    
@pytest.mark.parametrize("select_query", [
    "select a, b, c, 1+2+3 from xyz"
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
    printer.visit(expr_node, 0)
    
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
    printer.visit(column_node, 0)
    
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
    printer.visit(column_list_node, 0)
    
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
    ast_printer.visit(predicate_compare, 0)
    
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
    ast_printer.visit(predicate_not)
    

@pytest.mark.parametrize("valid_query", ["A=b AND D=e", "1*3+2 AND NOT(4>5 AND 1)"])
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
    printer.visit(predicate_and, 0)
    
@pytest.mark.parametrize("valid_query", ["1 + 2 OR a", " a > b OR c > d", "a = b AND c=d OR e = f"])
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
    printer.visit(predicate_or, 0)
    
    
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
    printer.visit(add_node)
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
    printer.visit(column_node)
    planner = ColumnListHandler(caller)
    result = planner.handle_column_node(column_node)
    assert result == {f"{column_node.name}": 1+1-2*4}
    
@pytest.mark.parametrize("valid_query", ["select a+1-2*4, a, a as c from xyz"]) 
def test_handle_column_node(valid_query, caller):
    parser = Parser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    column_list_node = parser.parse_column_list()
    printer = ASTPrinter()
    printer.visit(column_list_node)
    planner = ColumnListHandler(caller)
    result = planner.handle(column_list_node)
    assert result == {"columns": ("A + 1 - 2 * 4", "a", "c"), "data": (-6, 1, 1)}