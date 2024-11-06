
from dbcsv_server.connection import ConnectionIdentity
from dbcsv_server.db_controller import DBController
import pytest
from pathlib import Path

def test_return_connection_object_when_call_connect():
    con = ConnectionIdentity(Path(""))
    assert con.id

def test_status_after_connect():
    con = ConnectionIdentity()
    assert con.closed == False

def test_status_after_disconnect():
    con = ConnectionIdentity()
    con.close()
    assert con.closed == True

def test_can_not_execute_sql_on_connection_closed(con):
    assert con.closed == False
    con.close()
    db_controller = DBController()
    assert con.closed == True
    with pytest.raises() as e:
        assert db_controller.execute_query(con, "select * from abc")
        


