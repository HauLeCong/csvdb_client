
import pytest
from collections.abc import Iterator
from typing import Tuple, List

from dbcsv_server.query_engine.parser import QueryParser
from dbcsv_server.query_engine.ast_node import (
    FactorNode, 
    TermNode, 
    ArimethicNode, 
    ColumnNode, 
    ColumnListNode, 
    ColumnNameNode, 
    ColumnWildCardNode, 
    SelectNode, 
    FromNode, 
    WhereNode, 
    ExprNode
) 
from dbcsv_server.query_engine.token import Token
from dbcsv_server.query_engine.planner import QueryPlanner
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
    parser = QueryParser(valid_number)
    assert parser.scan_number(parser.current_character) == valid_number
 
    
@pytest.mark.parametrize("valid_string, expected", [("abc\r\n", "abc"), ("_abc\r\n", "_abc"), ("\"abc def\"\r\n", "abc def")])
def test_valid_string(valid_string, expected):
    """
    Test parser return valid string on scan
    """
    parser = QueryParser(valid_string)
    assert parser.scan_string() == expected.upper()

@pytest.mark.parametrize("invalid_string", ["\"abc"])
def test_not_closed_string(invalid_string):
    """
    Test return error when string not closed
    """
    parser = QueryParser(invalid_string)
    with pytest.raises(ValueError) as e:
        assert parser.scan_string()
    
    assert e.value.args[0] == f"Invalid token string was not closed"
    
def test_parse_func_iter_token():
    parser = QueryParser("select * from test")
    parser.scan()
    parser.parse()
    assert isinstance(parser.iter_token, Iterator)
    
@pytest.mark.parametrize("invalid_token", ["select a \r\n"])
def test_parse_factor_invalid_character(invalid_token):
    query_parser = QueryParser(invalid_token)
    query_parser.scan()
    query_parser.iter_token = iter(query_parser.token)
    query_parser.advance_token()
    query_parser.advance_token()
    with pytest.raises(ValueError) as e:
        assert query_parser.parse_factor()

@pytest.mark.parametrize("numeric, expected", [("1+ \r\n", 1.0), ("10+ \r\n", 10.0), ("1.2+ \r\n", 1.2)]) 
def test_parse_factor_single_digit(numeric, expected):
    parser = QueryParser(numeric)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    factor = parser.parse_factor()
    assert isinstance(factor, FactorNode)
    assert factor.expr == expected

@pytest.mark.parametrize("numeric, expected", [("1+2*3 \r\n", 1.0)])
def test_parse_term_single_digit(numeric, expected):
    parser = QueryParser(numeric)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    term = parser.parse_term()
    assert isinstance(term, TermNode)
    assert isinstance(term.left, FactorNode)
    assert term.left.expr == expected
   
@pytest.mark.parametrize("numeric, expected", [("1 ,\r\n", 1.0)]) 
def test_parse_aritmethic_single_digits(numeric, expected):
    parser = QueryParser(numeric)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    arimethic = parser.parse_arimethic()
    assert isinstance(arimethic, ArimethicNode)
    assert isinstance(arimethic.left, TermNode)
    assert isinstance(arimethic.left.left, FactorNode)
    assert arimethic.left.left.expr == expected

@pytest.mark.parametrize("valid_query", ["select 1+2*4 \r\n", "select 1*4+(7-8)"])
def test_parse_arimethic_full_flow(valid_query):
    parser = QueryParser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    arimethic = parser.parse_arimethic()
    assert isinstance(arimethic, ArimethicNode)
    print_tree(arimethic)

def test_visit_return_correct_hanlder():
    ast_handler = QueryPlanner()
    handler = ast_handler.get_handler("Arimethic")
    assert handler == ast_handler.handle_arimethic_node
    handler = ast_handler.get_handler("Term")
    assert handler == ast_handler.handle_term_node
    handler = ast_handler.get_handler("Factor")
    assert handler == ast_handler.handle_factor_node

def test_handle_simple_factor_node():
    factor = FactorNode(expr=10)
    ast_handler = QueryPlanner()
    handler = ast_handler.get_handler("Factor")
    value = handler(factor)
    assert value == 10

def test_handle_simple_term_node():
    term = TermNode(left=TermNode(left=FactorNode(10), right=None, operator=None), right=FactorNode(2), operator=Token.ASTERISK)
    ast_handler = QueryPlanner()
    handler = ast_handler.get_handler("Term")
    value = handler(term)
    assert value == 20
    
def test_handle_simple_arimethic_node():
    arimethic = ArimethicNode(
        left=ArimethicNode(
            left=TermNode(
                left=FactorNode(10), 
                right=None, 
                operator=None
            ),
            right = None,
            operator= None
        ),
        right = TermNode(
            left=FactorNode(2),
            right=None,
            operator=None    
        ), 
        operator=Token.PLUS)
    ast_handler = QueryPlanner()
    handler = ast_handler.get_handler("Arimethic")
    value = handler(arimethic)
    assert value == 12
    
@pytest.mark.parametrize("valid_query, expected", [
        ("select 1+2+3", 6), 
        ("select 1*3+4", 7), 
        ("select 7-3*4", -5), 
        ("select 7-(5 +6)", -4),
        ("select 1/4*5", 1.25),
    ]
)
def test_return_arimethic_node_value(valid_query, expected):
    parser = QueryParser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    arimethic = parser.parse_arimethic()
    assert isinstance(arimethic, ArimethicNode)
    ast_handler = QueryPlanner()
    s = arimethic.value(ast_handler)
    assert s == expected
    
@pytest.mark.parametrize("valid_query", [
    "select * from table", 
    "select abc as a from table", 
    """select "abc" as "a" from table """
    ]
)
def test_parse_column(valid_query):
    parser = QueryParser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    column_node = parser.parse_column()
    assert isinstance(column_node, ColumnNode)
    
@pytest.mark.parametrize("valid_query", [
        # "select a, b, c as c1 from table",
        "select 1 + 2 + 3, a, c from table"
    ]
)
def test_parse_column_list(valid_query):
    parser = QueryParser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    print(parser.current_token)
    column_list_node = parser.parse_column_list()
    # print(parser.token)
    # print(column_list_node)
    # print_tree(column_list_node)
    assert isinstance(column_list_node, ColumnListNode)
    
@pytest.mark.parametrize("from_clause", ["from abc", """from "xyz" """])
def test_parse_from_clause(from_clause):
    parser = QueryParser(from_clause)
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
    parser = QueryParser(select_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    select_clause = parser.parse_select_clause()
    print(select_clause)
    assert isinstance(select_clause, SelectNode)

def test_return_value_column_node():
    c = ColumnNode(
        expr=ExprNode(
            expr=ArimethicNode(
                left=ArimethicNode(
                    left=ArimethicNode(
                        left=TermNode(
                            left=FactorNode(expr=1.0), 
                            right=None, 
                            operator=None
                        ), 
                        right=None, 
                        operator=None
                    ), 
                    right=TermNode(
                        left=FactorNode(expr=2.0), 
                        right=None, operator=None), 
                    operator=Token.PLUS
                    ), 
                right=TermNode(
                    left=FactorNode(expr=3.0),
                    right=None, operator=None
                    ), 
                operator=Token.PLUS
            )
        ), 
        alias=None)   
    query_planner = QueryPlanner()
    result = query_planner.visit(c)
    print(result)
    
def test_return_value_column_name_node():
    column_node = ColumnNameNode(expr="A")
    query_planner = QueryPlanner()
    c = query_planner.visit(column_node)
    assert c == "A"
    
@pytest.mark.parametrize("valid_query", ["select a, b, 1 + 3  * 5 from xyz", "select 1 + 3 * 4, c, d from xyz"])
def test_return_column_list_node_value(valid_query):
    parser = QueryParser(valid_query)
    parser.scan()
    parser.iter_token =  iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    column_list_node = parser.parse_column_list()
    planner = QueryPlanner()
    column_list = planner.visit(column_list_node)
    print_tree(column_list_node)
    print(column_list)
    
@pytest.mark.parametrize("valid_query", ["select a, b, 1+2+3 from xyz"])
def test_return_select_node_value(valid_query):
    parser = QueryParser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    select_node = parser.parse_select_clause()
    planner = QueryPlanner()
    select = planner.visit(select_node)
    print(select)
    assert isinstance(select_node, SelectNode)    
    
@pytest.mark.parametrize("valid_query", ["select 1 + 3 - 4 * 2 from xyz"])
def test_calculate_height_of_node(valid_query):
    parser = QueryParser(valid_query)
    parser.scan()
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    arimethic_node = parser.parse_arimethic()
    print(arimethic_node)
    ast_printer = ASTPrinter()
    ast_printer.visit(arimethic_node, "1", 0)