import pytest
from dbcsv_server.query_engine.parser.scanner import Scanner
from dbcsv_server.query_engine.token import Token, ReservedWord


@pytest.mark.parametrize(
    "test_str, expected_value",
    [("1.23\r\n", 1.23), (" .123\r\n", 0.123), ("123.0e0 \r\n", 123.0), (" .123e0 \r\n", 0.123)],
)
def test_scan_literal_number(test_str, expected_value):
    scanner = Scanner(test_str)
    token_list = scanner.scan()
    assert token_list[0] == (Token.NUMBER_LITERAL, expected_value)


@pytest.mark.parametrize(
    "test_string, expected",
    [("abc \r\n", "abc"), ("a12d \r\n", "a12d"), ("_ads \r\n", "_ads")],
)
def test_scan_ident(test_string, expected):
    scanner = Scanner(test_string)
    token_list = scanner.scan()
    assert token_list[0] == (Token.IDENTIFIER, expected)


@pytest.mark.parametrize(
    "test_string, expected",
    [("SELECT \r\n", "SELECT"), ("FROM \r\n", "FROM"), ("NULL\r\n", "NULL")],
)
def test_scan_reserved_word(test_string, expected):
    scanner = Scanner(test_string)
    token_list = scanner.scan()
    assert token_list[0] == (ReservedWord[expected], None)


@pytest.mark.parametrize("test_query_string", "select * from abc.xyz \r\n")
def test_token_list_return(test_query_string):
    scanner = Scanner()
    token_list = scanner.scan()
    assert len(token_list) > 0
