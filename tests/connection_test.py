
import pathlib
import pytest
import dbapi2
from dbapi2 import Connection, Cursor
from dbapi2.exceptions import ProgramingError, DatabaseError


# User using connect to connect to db engine
def test_have_connect_method():
    assert "connect" in dbapi2.__dict__

# User enter missing path_file 
def test_raise_exception_not_provide_path():
    with pytest.raises(Exception):
        assert dbapi2.connect()
        
# User enter invalid path_file
@pytest.mark.parametrize("path_file", [(123, ), (True, ), (object())])
def test_raise_invalid_format(path_file):
    with pytest.raises(TypeError) as e:
        assert dbapi2.connect(path_file)
    error_msg = e.value.args[0]
    assert error_msg == "Invalid path_file, must be either string or Path"

# User enter valid path file
@pytest.mark.parametrize("path_file", [("abc", ), (pathlib.Path("abc"), )])
def test_valid_path_file(path_file):
    path_file = "abc"
    conn = dbapi2.connect(path_file)
    assert conn

# User retrieve cursor from connection
def test_call_return_cursor(dbapi2_connections):
    assert "cursor" in Connection.__dict__
    cursor = dbapi2_connections[0].cursor()
    assert isinstance(cursor, Cursor)

# Conenction close suing conteext manager
def test_clean_connection_context_manager(dbapi2_connections):
    with dbapi2_connections[0] as conn:
        assert conn.closed == 0
    assert conn.closed == 1
    
# Return error within context manager
def test_bubble_up_error(dbapi2_connections):
    with pytest.raises(ProgramingError) as e:
        with dbapi2_connections[0] as conn:
            assert 1/0

# Connection status: after connect shoudld be open
def test_connection_closed_after_call_close(dbapi2_connections):
    assert dbapi2_connections[0].closed == 0
    dbapi2_connections[0].close()
    assert dbapi2_connections[0].closed == 1
    
# User close connection while not commit transaction
def test_rollback_closed_connection(dbapi2_connections):
    assert False, "To be implement"
    
# User try to operate on closed connection
def test_operation_fail_after_connection_close(dbapi2_connections):
    assert dbapi2_connections[0].closed == 0
    dbapi2_connections[0].close()
    assert dbapi2_connections[0].closed == 1
    with pytest.raises(ZeroDivisionError) as e:
        assert dbapi2_connections[0].cursor()
    error_msg = e.value.args[0]
    assert error_msg == "Cannot operate on closed connection"
    
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