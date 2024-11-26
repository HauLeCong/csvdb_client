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


@pytest.mark.parametrize("path_file", [(123,), (True,), (object())])
def test_raise_invalid_format(path_file):
    """
    3. >>> User enter invalid path file format
    test_raise_invalid_format()
    """
    with pytest.raises(TypeError) as e:
        assert dbcsv.connect(path_file)
    error_msg = e.value.args[0]
    assert error_msg == "Invalid path_file, must be either string or Path"


@pytest.mark.parametrize("path_file", [("abc",), (pathlib.Path("abc"),)])
def test_valid_path_file(path_file):
    """
    4. >>> User enter valid format
    test_valid_path_file
    """
    path_file = "abc"
    conn = dbcsv.connect(path_file)
    assert isinstance(conn, Connection)


def test_call_return_cursor(dbapi2_connection1):
    """
    5. >>> User try to create cursor obj
    test_call_return_cursor()
    """
    assert "cursor" in Connection.__dict__
    cursor = dbapi2_connection1.cursor()
    assert isinstance(cursor, Cursor)


def test_clean_connection_context_manager(dbapi2_connection1):
    """
    6. >>> User using connection as context manager, test closed status after exit context
    test_clean_connection_context_manager()
    """
    with dbapi2_connection1 as conn:
        assert conn.closed == 0
    assert conn.closed == 1


def test_bubble_up_error(dbapi2_connection1):
    """
    7. >>> While using connection, user make an exception - test that exception be not supressed
    test_bubble_up_error()
    """
    with pytest.raises(Exception) as e:
        with dbapi2_connection1 as conn:
            assert 1 / 0
        assert conn.closed == 1


def test_connection_closed_after_call_close(dbapi2_connection1):
    """
    8. >>> User try to close a connection
    test_connection_closed_after_call_close()
    """
    assert dbapi2_connection1.closed == 0
    dbapi2_connection1.close()
    assert dbapi2_connection1.closed == 1


def test_create_cursor_fail_on_connection_closed(dbapi2_connection1):
    """
        9. >>> User try to operate on on closed connection
    test_create_cursor_fail_on_connection_closed()
    """
    assert dbapi2_connection1.closed == 0
    dbapi2_connection1.close()
    assert dbapi2_connection1.closed == 1
    with pytest.raises(ProgramingError) as e:
        assert dbapi2_connection1.cursor()
    error_msg = e.value.args[0]

    assert error_msg == "Cannot operate on closed connection."


@pytest.mark.skip("Wait api for API implemention")
def test_rollback_on_closed_connection(
    dbapi2_connection1, mock_insert_data, mocke, mocker
):
    """
    11. User close connection without commit
    test_rollback_on_closed_connection()
    """
    assert dbapi2_connection1.closed == 0
    cursor = dbapi2_connection1.cursor()
    mock_call = mocker.patch("dbapi2_connection1.rollback")
    cursor.execute("insert into test values(?, ?, ?)", mock_insert_data)
    start_row_num = cursor.row_number
    # Call commit on close
    dbapi2_connection1.close()
    cursor.execute("select * from test where id=?", mock_insert_data[0])
    assert cursor.row_number == start_row_num
    assert mock_call.assert_called_once_with()


@pytest.mark.skip("Wait api for API implemention")
def test_commit_insert_data(dbapi2_connection1, dbapi2_connection2, mock_insert_data):
    """
    12. User commit insert transaction
    test_commit_insert_data()
    """
    assert dbapi2_connection1.closed == 0
    cursor = dbapi2_connection1.cursor()
    cursor.execute(
        """Insert into test_table values(?) where id = ?""", mock_insert_data
    )
    # Autoo commit = T|F
    dbapi2_connection1.commit()
    cursor2 = dbapi2_connection2.cursor()
    cursor2.execute("""Select * from test_table where id = ?""", (id,))
    assert cursor.row_number == cursor2.row_number + 1


@pytest.mark.skip("Wait api for API implemention")
def test_havent_commit_insert_data(
    dbapi2_connection1, dbapi2_connection2, mock_insert_data
):
    """
    13. User not uncommit data expect differnet result on 2 cursor
    test_uncommit_insert_data()
    """
    cursor = dbapi2_connection1.cursor()
    cursor.execute("""Insert into test values(?) where id = ?""", mock_insert_data)
    # Autoo commit = T|F
    cursor2 = dbapi2_connection2.cursor()
    cursor2.execute("Select * from test_table where id = ?", (id,))
    assert cursor.row_number > cursor2.row_number


@pytest.mark.skip("Wait api for API implemention")
def test_commit_create_table(dbapi2_connection1, dbapi2_connection2):
    """
    14. User commit a create table command
    test_commit_create_table()
    """
    cursor = dbapi2_connection1.cursor()
    cursor.execute("Create table test (col1 string, col2 string)")
    dbapi2_connection1.commit()
    cursor2 = dbapi2_connection2.cursor()
    assert cursor2.execute("Select * from test;")


@pytest.mark.skip("Wait api for API implemention")
def test_uncommit_create_table(dbapi2_connection1, dbapi2_connection2):
    """
    15. User don't commit while create table
    test_uncommit_create_table()
    """
    cursor = dbapi2_connection1.cursor()
    cursor.execute("Create table test (col1 string, col2 string)")
    cursor2 = dbapi2_connection2.cursor()
    with pytest.raises(DatabaseError) as e:
        cursor2.execute("Select * from test;")
    error_msg = e.value.args[0]
    assert error_msg == "table not exists"


@pytest.mark.skip("Wait for API implemention")
def test_full_flow():
    con = Connection()
    cursor = con.cursor()
    cursor.execute("select * from ")
    assert False, "Not implemented"


@pytest.mark.skip("Wait api for API implemention")
def test_rollback_insert_data():
    # Autoo commit = T|F
    assert False, "Not implemented"


def test_get_connection_id_on_connect():
    import requests

    rs = requests.get("http://127.0.0.1/connect")
    data = rs.json()
    assert data
