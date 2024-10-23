
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

# User then get a Connection obj to interact with db engine
def test_return_connection_obj():
    conn = dbapi2.connect("abc")
    assert isinstance(conn, Connection)

# User retrieve cursor from connection
def test_call_return_cursor():
    assert "cursor" in Connection.__dict__
    conn = dbapi2.connect("abc")
    cursor = conn.cursor()
    assert isinstance(cursor, Cursor)

# Conenction close suing conteext manager
def test_clean_connection_context_manager():
    with dbapi2.connect("abc") as conn:
        assert conn.closed == 0
    assert conn.closed == 1
    
# Return error within context manager
def test_bubble_up_error():
    with pytest.raises(ProgramingError) as e:
        with dbapi2.connect("abc") as con:
            assert 1/0

# Connection status: after connect shoudld be open
def test_connection_closed_after_call_close():
    conn = dbapi2.connect("abc")
    assert conn.closed == 0
    conn.close()
    assert conn.closed == 1
    
# User try to operate on closed connection
def test_operation_fail_after_connection_close():
    conn = dbapi2.connect("abc")
    assert conn.closed == 0
    conn.close()
    assert conn.closed == 1
    with pytest.raises(ProgramingError) as e:
        assert conn.cursor()
    error_msg = e.value.args[0]
    assert error_msg == "Cannot operate on closed connection"
    
# User commit transaction
# Test only if database-engine support transaction else pass
def test_commit_insert_data(data, id):
    conn = dbapi2.connect("abc")
    cursor = conn.cursor()
    cursor.execute("""Insert into test_table values(?) where id = ?""", (data, id))
    conn.commit()
    conn2 = dbapi2.connect("abc")
    cursor2 = conn2.cursor()
    cursor2.execute("""Select * from test_table where id = ?""", (id, ))
    assert cursor.row_number == cursor2.row_number + 1
    
def test_uncommit_insert_data(data, id):
    conn = dbapi2.connect("abc")
    cursor = conn.cursor()
    cursor.execute("""Insert into test values(?) where id = ?""", (data, id))
    conn2 = dbapi2.connect("abc")
    cursor2 = conn2.cursor()
    cursor2.execute("Select * from test_table where id = ?", (id, ))
    assert cursor.row_number > cursor2.row_number

def test_commit_create_table():
    conn = dbapi2.connect("abc")
    cursor = conn.cursor()
    cursor.execute("Create table test (col1 string, col2 string)")
    conn.commit()
    conn2 = dbapi2.connect("abc")
    cursor2 = conn2.cursor()
    assert cursor2.execute("Select * from test;")
    
def test_uncommit_create_table():
    conn = dbapi2.connect("abc")
    cursor = conn.cursor()
    cursor.execute("Create table test (col1 string, col2 string)")
    conn2 = dbapi2.connect("abc")
    cursor2 = conn2.cursor()
    with pytest.raises(DatabaseError) as e:
        cursor2.execute("Select * from test;")
    error_msg = e.value.args[0]
    assert error_msg == "table not exists"

# def test_commit_delete_data(data, id):
    # pass

# def test_commit_update_data(data):
#     pass

def test_uncommit_insert_data(data):
    assert False, "Not implemented"

def test_uncommit_update_date(data):
    assert False, "Not implemented"

def test_uncommit_delete_data(data):
    assert False, "Not implemented"

def test_rollback():
    assert False, "Not implemented"