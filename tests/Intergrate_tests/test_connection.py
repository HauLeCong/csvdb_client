
import pathlib
import pytest
import dbcsv
from dbcsv import Connection, Cursor
from dbcsv.exceptions import ProgramingError, DatabaseError

def test_have_connect_method():
    """
        1. >>> User try to use connect method to connect to db engine
        test_have_connect_method():
    """
    assert "connect" in dbcsv.__dict__

def test_raise_exception_not_provide_path():
    """
        2. >>> User didn't enter path file
        test_raise_exception_not_provide_path()
    """
    with pytest.raises(Exception):
        assert dbcsv.connect()
        
# User enter invalid path_file
@pytest.mark.parametrize("path_file", [(123, ), (True, ), (object())])
def test_raise_invalid_format(path_file):
    """
        3. >>> User enter invalid path file format
        test_raise_invalid_format()
    """
    with pytest.raises(TypeError) as e:
        assert dbcsv.connect(path_file)
    error_msg = e.value.args[0]
    assert error_msg == "Invalid path_file, must be either string or Path"

# User enter valid path file
@pytest.mark.parametrize("path_file", [("abc", ), (pathlib.Path("abc"), )])
def test_valid_path_file(path_file):
    """
        4. >>> User enter valid format 
        test_valid_path_file
    """
    path_file = "abc"
    conn = dbcsv.connect(path_file)
    assert conn

# User retrieve cursor from connection
def test_call_return_cursor(dbapi2_connections):
    """
        5. >>> User try to create cursor obj
        test_call_return_cursor()
    """
    assert "cursor" in Connection.__dict__
    cursor = dbapi2_connections[0].cursor()
    assert isinstance(cursor, Cursor)
    
def test_clean_connection_context_manager(dbapi2_connections):
    """
        6. >>> User using connection as context manager, test closed status after exit context
        test_clean_connection_context_manager()
    """
    with dbapi2_connections[0] as conn:
        assert conn.closed == 0
    assert conn.closed == 1
    
def test_bubble_up_error(dbapi2_connections):
    """
        7. >>> While using connection, user make an exception - test that exception be not supressed
        test_bubble_up_error()
    """
    with pytest.raises(ProgramingError) as e:
        with dbapi2_connections[0] as conn:
            assert 1/0

def test_connection_closed_after_call_close(dbapi2_connections):
    """
        8. >>> User try to close a connection
        test_connection_closed_after_call_close()
    """
    assert dbapi2_connections[0].closed == 0
    dbapi2_connections[0].close()
    assert dbapi2_connections[0].closed == 1


def test_operation_fail_after_connection_close(dbapi2_connections):
    assert dbapi2_connections[0].closed == 0
    dbapi2_connections[0].close()
    assert dbapi2_connections[0].closed == 1
    with pytest.raises(ProgramingError) as e:
        assert dbapi2_connections[0].cursor()
    error_msg = e.value.args[0]
    assert error_msg == "Cannot operate on closed connection"

# User close connection while not commit transaction
def test_rollback_closed_connection(dbapi2_connections):
    assert False, "To be implement"
    
# User commit transaction
# Test only if database-engine support transaction else pass
def test_commit_insert_data(dbapi2_connections, mock_insert_data):
    assert dbapi2_connections[0].closed == 0
    cursor = dbapi2_connections[0].cursor()
    cursor.execute("""Insert into test_table values(?) where id = ?""", mock_insert_data)
    dbapi2_connections[0].commit()
    cursor2 = dbapi2_connections[1].cursor()
    cursor2.execute("""Select * from test_table where id = ?""", (id, ))
    assert cursor.row_number == cursor2.row_number + 1
    
def test_uncommit_insert_data(dbapi2_connections, mock_insert_data):
    cursor = dbapi2_connections[0].cursor()
    cursor.execute("""Insert into test values(?) where id = ?""", mock_insert_data)
    cursor2 = dbapi2_connections[1].cursor()
    cursor2.execute("Select * from test_table where id = ?", (id, ))
    assert cursor.row_number > cursor2.row_number

def test_commit_create_table(dbapi2_connections):
    cursor = dbapi2_connections[0].cursor()
    cursor.execute("Create table test (col1 string, col2 string)")
    dbapi2_connections[0].commit()
    cursor2 = dbapi2_connections[1].cursor()
    assert cursor2.execute("Select * from test;")
    
def test_uncommit_create_table(dbapi2_connections):
    cursor = dbapi2_connections[0].cursor()
    cursor.execute("Create table test (col1 string, col2 string)")
    cursor2 = dbapi2_connections[1].cursor()
    with pytest.raises(DatabaseError) as e:
        cursor2.execute("Select * from test;")
    error_msg = e.value.args[0]
    assert error_msg == "table not exists"

# def test_commit_delete_data(data, id):
    # pass

# def test_commit_update_data(data):
#     pass

def test_uncommit_insert_data():
    assert False, "Not implemented"

def test_uncommit_update_date():
    assert False, "Not implemented"

def test_uncommit_delete_data():
    assert False, "Not implemented"

def test_rollback():
    assert False, "Not implemented"
    