import pytest
import dbapi2
from dbapi2.exceptions import ProgramingError, DatabaseError
from dbapi2 import Connection, Cursor
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
        2. >>> Each cursor have its description from last executed query
        test_cursor_have_description_attr()
    """
    cursor = dbapi2_connections[0].cursor()
    assert "description" in cursor.__dict__
    assert cursor.description == None
    

def test_cursor_description_match_columns_name(dbapi2_connections, mock_data_file):
    """
        3. >>> User try to view description from whenever they execute a new query
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


