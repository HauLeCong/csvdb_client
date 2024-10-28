import pytest
from dbcsv.exceptions import ProgramingError, DatabaseError
from dbcsv import Cursor
import pandas as pd
import random


def test_create_cursor_from_connection(dbapi2_connection1):
    """
    1. >>> User try to create a cursor
    test_create_cursor_from_connection()
    """
    cursor = dbapi2_connection1.cursor()
    assert cursor
    assert isinstance(cursor, Cursor)


def test_cursor_have_description_attr(dbapi2_connection1):
    """
    2. >>> Each cursor have its own description default None
    test_cursor_have_description_attr()
    """
    cursor = dbapi2_connection1.cursor()
    assert cursor.description == None


@pytest.mark.parametrize(
    "sql,parameters", [(1, None), (True, None), (1.0, None)]
)
def test_call_execute_invalid_query_type(dbapi2_connection1, sql, parameters):
    """
    3. >>> User try to execute invalid query
    test_call_execute_invalid_query_type()
    """
    cursor = dbapi2_connection1.cursor()
    with pytest.raises(TypeError):
        assert cursor.execute(sql, parameters)


@pytest.mark.parametrize(
    "sql,parameters",
    [
        ("select 1", None),
        ("select * from user", None),
        ("abc", None),
    ],
)
def test_call_execute_with_valid_query(
    dbapi2_connection1, mock_execute_sql, sql, parameters
):
    """
    4. >>> User execute valid query format - string
    test_call_execute_with_valid_query()
    """
    cursor = dbapi2_connection1.cursor()
    data = cursor.execute(sql, parameters)
    print(data)


@pytest.mark.parametrize(
    "sql,parameters", [("select 1", 1), ("select 1", True)]
)
def test_call_execute_invalid_parameters(dbapi2_connection1, sql, parameters):
    """
    5. >>> User execute query with invalid paramters - parameter is not list, tuple or Row
    test_call_execute_invalid_parameters()
    """
    cursor = dbapi2_connection1.cursor()
    with pytest.raises(ValueError):
        assert cursor.execute(sql, parameters)


@pytest.mark.parametrize(
    "sql,parameters",
    [("select 1", ("1", "2")), ("select 1", ["1", "2"]), ("select 1", "abc")],
)
def test_call_execute_valid_parameters(
    dbapi2_connection1, mock_execute_sql, sql, parameters
):
    """
    6. >>> User execute valid query and paramters
    """
    cursor = dbapi2_connection1.cursor()
    assert cursor.execute(sql, parameters)


@pytest.mark.skip("Wait for API implemention")
def test_cursor_description_match_columns_name(
    dbapi2_connection1, mock_data_file
):
    """
    7. >>> User try to view description from whenever they execute a new query
    test_cursor_description_match_columns_name()
    """
    cursor = dbapi2_connection1.cursor()
    cursor.execute("select * from test;", ())
    cols = [col[0] for col in cursor.description]
    df = pd.read_csv(mock_data_file)
    assert len(cols) == len(list(df.columns))
    for col in cols:
        assert col in list(df.columns)


@pytest.mark.skip("Wait for API implemention")
def test_cursor_description_match_return_data_type(dbapi2_connection1):
    """
    8. >>> User read datatype return by cursor
    test_cursor_description_match_return_data_type()
    """
    assert False, "TO DO"


def test_close_cursor(dbapi2_connection1):
    """
    9. >>> User try to close a cursor
    test_close_cursor()
    """
    cursor = dbapi2_connection1.cursor()
    assert cursor._closed == 0
    cursor.close()
    assert cursor._closed == 1


def test_raise_error_trying_query_on_connection_close(dbapi2_connection1):
    """
    10. >>> User try to query on connection closed
    test_raise_error_trying_query_on_connection_close()
    """
    cursor = dbapi2_connection1.cursor()
    assert cursor.connection.closed == 0
    dbapi2_connection1.close()
    assert cursor.connection.closed == 1
    with pytest.raises(ProgramingError) as e:
        assert cursor.execute("select 1")
    error_msg = e.value.args[0]
    assert error_msg == "Cannot operate on closed connection."


def test_raise_error_trying_operate_on_cursor_closed(dbapi2_connection1):
    """
    11. >>> User try to query on cursor closed
    test_raise_error_trying_operate_on_cursor_closed()
    """
    cursor = dbapi2_connection1.cursor()
    assert cursor._closed == 0
    cursor.close()
    assert cursor._closed == 1
    with pytest.raises(ProgramingError) as e:
        assert cursor.execute("select 1")
    error_msg = e.value.args[0]
    assert error_msg == "Cannot operate on a closed cursor."


def test_fetchone_on_query_result(dbapi2_connection1, mock_execute_sql):
    """
    12. >>> User fetchone data
    test_fetchone_on_query_result()
    """
    cursor = dbapi2_connection1.cursor()
    assert cursor._closed == 0
    test_cursor = cursor.execute("Select * from test")
    for r in test_cursor:
        assert r == cursor.fetchone()


@pytest.mark.parametrize("number", ["abc", 1.0, b"def"])
def test_user_give_wrong_format_arraysize(dbapi2_connection1, number):
    """
    13. >>> User give wrong type setting arraysize
    test_user_give_wrong_format_arraysize()
    """
    cursor = dbapi2_connection1.cursor()
    assert cursor.arraysize == 1
    with pytest.raises(TypeError) as e:
        cursor.arraysize = number


@pytest.mark.parametrize("number", [1, 10, 2, True])
def test_user_give_valid_arraysize(dbapi2_connection1, number):
    """
    14. >>> User give valid type for arraysize
    test_user_give_valid_arraysize()
    """
    cursor = dbapi2_connection1.cursor()
    assert cursor.arraysize == 1
    cursor.arraysize = number
    assert cursor.arraysize == number


@pytest.mark.parametrize("number", ["abc", 1.0, b"def"])
def test_user_call_fetchmany_witn_invalid_format(
    dbapi2_connection1, number, mock_execute_sql
):
    """
    15. >>> User call fetchmany with invalid type
    test_user_call_fetchmany_witn_invalid_format()
    """
    cursor = dbapi2_connection1.cursor()
    cursor.execute("select * from test")
    with pytest.raises(TypeError) as e:
        assert cursor.fetchmany(number)


@pytest.mark.parametrize(
    "number",
    [
        random.randint(1, 10),
        random.randint(1, 10),
        random.randint(1, 10),
        random.randint(1, 10),
    ],
)
def test_fetchmany_on_query_result(
    dbapi2_connection1, number, mock_execute_sql
):
    """
    16. >>> User call fetchmany and expect the result
    test_fetchmany_on_query_result()
    """
    cursor = dbapi2_connection1.cursor()
    cursor2 = dbapi2_connection1.cursor()
    cursor.execute("Select * from test")
    cursor2 = cursor.execute("Select * from test")
    check_list = list(cursor2)
    assert check_list[:number] == cursor.fetchmany(number)


@pytest.mark.parametrize(
    "fetch_time", [random.randint(1, 4), random.randint(2, 4)]
)
def test_call_fetchmany_multiple_time(
    dbapi2_connection1, fetch_time, mock_execute_sql
):
    """
    17. >>> User call fetchmany multiple time
    test_call_fetchmany_multiple_time()
    """
    cursor = dbapi2_connection1.cursor()
    cursor.execute("select * from test")
    cursor2 = dbapi2_connection1.cursor()
    check_list = list(cursor2.execute("select * from user"))
    start_fetch = 0
    while fetch_time > 0:
        fetch_row = random.randint(2, 10)
        assert check_list[
            start_fetch : start_fetch + fetch_row
        ] == cursor.fetchmany(fetch_row)
        start_fetch += fetch_row
        fetch_time -= 1


@pytest.mark.parametrize(
    "number", [random.randint(2, 5), random.randint(2, 5), random.randint(2, 5)]
)
def test_change_arraysize_apply_call_fetchmany(
    dbapi2_connection1, number, mock_execute_sql
):
    """
    18. >>> User call fetchmany then change arraysize
    test_default_arraysize_apply_call_fetchmany()
    """
    cursor = dbapi2_connection1.cursor()
    cursor2 = dbapi2_connection1.cursor()
    assert cursor.arraysize == 1
    cursor2 = cursor.execute("select * from user")
    check_list = list(cursor2)
    assert check_list[: cursor.arraysize] == cursor.fetchmany()
    cursor2 = cursor.execute("select * from user")
    check_list = list(cursor2)
    cursor.arraysize = number
    assert number == cursor.arraysize
    assert check_list[: cursor.arraysize] == cursor.fetchmany()


def test_change_call_fetchmany_with_size_change_arraysize(dbapi2_connection1):
    """
    19. >>> User called fetchmany with size, also change arraysize so that consists with following fetchmany
    """
    cursor = dbapi2_connection1.cursor()
    cursor.execute("select * from test")
    assert cursor.arraysize == 1
    cursor.fetchmany(10)
    assert cursor.arraysize == 10


@pytest.mark.skip("Wait for API implemention")
def test_execute_multiple_time_reset(dbapi2_connection1, mock_execute_sql):
    """
    20. >>> User call execute sql multiple time - need to check that cursor is reset on each call
    test_execute_multiple_time_reset
    """
    cursor = dbapi2_connection1.cursor()


@pytest.mark.skip("Wait for API implemention")
def test_real_implement_execute_sql():
    assert False, "TO DO - Fullflow test - to be implement"


@pytest.mark.skip("Wait for API implemention")
def test_set_output_size():
    assert False, "TO DO"


@pytest.mark.skip("Wait for API implemention")
def test_set_input_size():
    assert False, "TO DO"


@pytest.mark.skip("Wait for API implemention")
def test_execute_select_query_by_id(dbapi2_connection1, mock_data_file):
    assert False, "TO DO"


@pytest.mark.skip("Wait for API implemention")
def test_execute_select_all():
    assert False, "TO DO"


@pytest.mark.skip("Wait for API implemention")
def test_execute_create_table():
    assert False, "TO DO"


@pytest.mark.skip("Wait for API implemention")
def test_execute_insert():
    assert False, "TO DO"
