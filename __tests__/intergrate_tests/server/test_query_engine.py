from dbcsv_server.query_engine.parser import QueryParser
import pytest
import re

from dbcsv_server.query_engine.parser import ReservedWord, Token
from dbcsv_server.query_engine.ast_node import FactorNode

# 
@pytest.mark.parametrize("invalid_str", [1, None, True])
def test_invalid_query_string(invalid_str):
    with pytest.raises(ValueError) as e:
        assert QueryParser(invalid_str)
    assert e.value.args[0] == "Only accept string argument"

@pytest.mark.parametrize("valid_str", ["123", "abc", "select *", "asdf {}".format(123)])
def test_giving_valid_string(valid_str):
    query_parser = QueryParser(valid_str)
    assert query_parser.query_string == valid_str.upper() + "\r\n"
    assert query_parser.current_character == valid_str.upper()[0]

@pytest.mark.parametrize("valid_str, expected", [(" 123", "123"), (" 1", "1")])
def test_peek_next_return_expected_literal_number(valid_str, expected):
    query_parser = QueryParser(valid_str)
    literal_number = query_parser.peek_next("", re.compile(r"[^\d]"))
    assert literal_number == expected
    
@pytest.mark.parametrize("unsupport_token", ["|", "`", "~"])
def test_raise_error_while_giving_invalid_token(unsupport_token):
    query_parser = QueryParser(unsupport_token)
    with pytest.raises(ValueError) as e:
        assert query_parser.scan()
    assert e.value.args[0] == f"Not support character {unsupport_token} at line 1 position 0"

@pytest.mark.parametrize("invalid", ["abc~", "gh`"])
def test_return_invalid_identifier(invalid):
    query_parser = QueryParser(invalid)
    with pytest.raises(ValueError) as e:
        assert query_parser.scan()
    assert e.value.args[0] == f"Invalid token {invalid.upper()}"

@pytest.mark.parametrize("invalid", ["select ''' "])
def test_unclose_liter_string(invalid):
    query_parser = QueryParser(invalid)
    with pytest.raises(ValueError) as e:
        assert query_parser.scan()
    assert e.value.args[0] == f"Literal not closed"

@pytest.mark.parametrize("valid_query, expect_token_list", 
    [
        (
            "select * from information_schema", [
                (ReservedWord.SELECT, ),
                (Token.ASTERISK, ),
                (ReservedWord.FROM, ), 
                (Token.INDENTIFIER, "INFORMATION_SCHEMA")
            ]
        ),
        (
            "select 1+2-3",[
                (ReservedWord.SELECT, ),
                (Token.NUMBER_LITERAL, 1.0),
                (Token.PLUS, ),
                (Token.NUMBER_LITERAL, 2.0),
                (Token.MINUS, ),
                (Token.NUMBER_LITERAL, 3.0)
            ]
        ),
        (
            "select 1, \'abc\' as test from a",[
                (ReservedWord.SELECT, ),
                (Token.NUMBER_LITERAL, 1.0),
                (Token.COMMA, ),
                (Token.STRING_LITERAL, "ABC"),
                (ReservedWord.AS, ),
                (Token.INDENTIFIER, "TEST"),
                (ReservedWord.FROM, ),
                (Token.INDENTIFIER, "A")
            ]
        ),
        (
            "select 1.2 + 3.5", [
                (ReservedWord.SELECT, ),
                (Token.NUMBER_LITERAL, 1.2),
                (Token.PLUS, ),
                (Token.NUMBER_LITERAL, 3.5)
            ]
        )
    ]
)
def test_return_expected_list_of_token(valid_query, expect_token_list):
    query_parser = QueryParser(valid_query)
    query_parser.scan()
    assert query_parser.token == expect_token_list

@pytest.mark.parametrize("invalid_query", ["1 + 2 + 3", "hello world"])
def test_giving_invalid_query(invalid_query):
    parser = QueryParser(invalid_query)
    parser.scan()
    with pytest.raises(ValueError) as e:
        assert parser.parse()
    assert e.value.args[0] == f"Invalid query expect SELECT or CREATE TABLE command got f{parser.current_token}"
    
@pytest.mark.parametrize("mock_parser", ["select * from abc"], indirect = True)
def test_call_parse_select_on_valid_select_clause(mock_parser):
    mock_parser.scan()
    assert mock_parser.parse()

@pytest.mark.parametrize("mock_parser", ["create table abc"], indirect=True)
def test_call_parse_create_table_on_valid_query(mock_parser):
    mock_parser.scan()
    print(mock_parser.token)
    assert mock_parser.parse()

