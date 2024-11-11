
import pytest
from collections.abc import Iterator

from dbcsv_server.query_engine import QueryParser
from dbcsv_server.ast_node import FactorNode, TermNode, ArimethicNode

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
    print(parser.token)
    arimethic = parser.parse_arimethic()
    assert isinstance(arimethic, ArimethicNode)
    assert isinstance(arimethic.left, TermNode)
    assert isinstance(arimethic.left.left, FactorNode)
    assert arimethic.left.left.expr == expected

@pytest.mark.parametrize("valid_query", ["select 1+2*4 \r\n", "select 1*4+(7-8)"])
def test_parse_arimethic_full_flow(valid_query):
    parser = QueryParser(valid_query)
    parser.scan()
    print(parser.token)
    parser.iter_token = iter(parser.token)
    parser.advance_token()
    parser.advance_token()
    arimethic = parser.parse_arimethic()
    assert isinstance(arimethic, ArimethicNode)
    print(arimethic)
    tree = {}
    level = 0
    def print_node(obj):
        if not hasattr(obj, "left"):
            # Also check if have right
            print(f"level {level}:")
            print(f"left {obj.left.name}")
        else:
            print(obj.left)
            _hold = obj.left
            print_node(_hold)
    print_node(arimethic)
    
# visitor pattern
# visit
# get_hanler
# visit node -> get handler -> handler() 

