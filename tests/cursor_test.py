import pytest
import dbapi2
from dbapi2.exceptions import ProgramingError, DatabaseError
from dbapi2 import Connection, Cursor


def test_create_cursor_from_connection():
    conn = dbapi2.connect("abc")
    assert conn.cursor()