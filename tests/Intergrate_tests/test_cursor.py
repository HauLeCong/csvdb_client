import pytest
import dbcsv
from dbcsv.exceptions import ProgramingError, DatabaseError
from dbcsv import Connection, Cursor
import pandas as pd

def test_create_cursor_from_connection(dbapi2_connections):
    """
        1. >>> User try to create a cursor
        test_create_cursor_from_connection()
    """
    cursor = dbapi2_connections[0].cursor()
    assert cursor
    assert isinstance(cursor, Cursor)

def test_cursor_have_description_attr(dbapi2_connections):
    """
        2. >>> Each cursor have its own description default None
        test_cursor_have_description_attr()
    """
    cursor = dbapi2_connections[0].cursor()
    assert cursor.description == None
    
@pytest.mark.parametrize("sql,parameters", [(1, None), (True, None), (1.0, None), ("select * from %s".format("table_name"),None)])
def test_call_execute_invalid_query_type(dbapi2_connections, sql, parameters):
    """
        Customer try to execute invalid query
        test_call_execute_invalid_query_type()
    """
    cursor = dbapi2_connections[0].cursor()
    with pytest.raises(TypeError):
        assert cursor.execute(sql,parameters)
                
@pytest.mark.parametrize("sql,parameters", [("select 1", None), ("select * from user", None), ("abc", None)])
def test_call_execute_with_valid_query(dbapi2_connections, sql, parameters):
    """
        Customer execute valid query format - string
        test_call_execute_with_valid_query()
    """   
    cursor = dbapi2_connections[0].cursor()
    assert cursor.execute(sql, parameters)

@pytest.mark.parametrize("sql,parameters", [("select 1", 1), ("select 1", True)])
def test_call_execute_invalid_parameters(dbapi2_connections, sql, parameters):
    """
        Customer execute query with invalid paramters - parameter is not list, tuple or Row
        test_call_execute_invalid_parameters()
    """
    cursor = dbapi2_connections[0].cursor()
    with pytest.raises(ValueError):
        assert cursor.execute(sql, parameters)

@pytest.mark.parametrize("sql,parameters", [("select 1", ("1", "2")), ("select 1", ["1", "2"]), ("select 1", "abc")])
def test_call_execute_valid_parameters(dbapi2_connections, sql, parameters):
    """
        Customer execute valid query and paramters
    """
    cursor = dbapi2_connections[0].cursor()
    assert cursor.execute(sql, parameters)
    
def test_cursor_description_match_columns_name(dbapi2_connections, mock_data_file):
    """
        xx. >>> User try to view description from whenever they execute a new query
        test_cursor_description_match_columns_name()
    """    
    cursor = dbapi2_connections[0].cursor()
    cursor.execute("select * from test;", ())
    cols = [col[0] for col in cursor.description]
    df = pd.read_csv(mock_data_file)
    assert len(cols) == len(list(df.columns))
    for col in cols:
        assert col in list(df.columns)

def test_raise_error_trying_query_on_connectio_close(dbapi2_connections):
    cursor = dbapi2_connections[0].cursor()
    assert cursor.connection.closed == 0
    dbapi2_connections[0].close()
    assert cursor.connection.closed == 1
    with pytest.raises(ProgramingError) as e:
        assert cursor.execute("select 1")
    error_msg = e.value.args[0]
    assert error_msg == "Cannot operate on closed connection"
    
def test_raise_error_trying_operate_on_cursor_close(dbapi2_connections):
    cursor = dbapi2_connections[0].cursor()
    assert cursor.closed == 0
    cursor.close()
    assert cursor.closed == 1
    with pytest.raises(ProgramingError) as e:
        assert cursor.execute("select 1")
    error_msg = e.value.args[0]
    assert error_msg == "Cannot operate on closed cursor"

def test_execute_select_query_by_id(dbapi2_connections, mock_data_file):
    pass

def test_execute_select_all():
    pass

def test_execute_create_table():
    pass

def test_execute_insert():
    pass


