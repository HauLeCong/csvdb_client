import pytest
from dbcsv import Connection, Cursor


@pytest.mark.skip("Wait implement")
def test_create_a_cursor_from_connection(connection):
    cursor = connection.cursor()
    assert (cursor, Cursor)


@pytest.mark.skip("Wait implement")
def test_return_a_str_from_prepare_query(connection, sql, params):
    cursor = connection.cursor()
    cursor._prepare_query_param(sql, params)
    assert isinstance(sql, str)


@pytest.mark.skip("Wait implement")
@pytest.mark.parametrize(
    "sql,params,expected_sql", [("", (), ""), ("", [], ""), ("", "", "")]
)
def test_return_correct_sql_statement(connection, sql, params, expected_sql):
    cursor = connection.cursor()
    return_sql = cursor._prepare_query_param(sql, params)
    assert return_sql == expected_sql
