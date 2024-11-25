
from dbcsv_server.connection import ConnectionIdentity
from dbcsv_server.db_controller import DBController
import pytest
from pathlib import Path

def test_return_connection_object_when_call_connect():
    con = ConnectionIdentity(Path(""))
    assert con.id

def test_status_after_connect():
    con = ConnectionIdentity(Path(""))
    assert con.closed == False

def test_status_after_disconnect():
    con = ConnectionIdentity(Path(""))
    con.close()
    assert con.closed == True

def test_can_not_execute_sql_on_connection_closed(con):
    assert con.closed == False
    con.close()
    db_controller = DBController()
    assert con.closed == True
    with pytest.raises(RuntimeError) as e:
        assert db_controller.execute_query(con, "select * from abc")
        
def test_create_table(con):
    assert con.closed == False
    db_controller = DBController()
    db_controller.execute_query(con, "CREATE TABLE test_database.test_table (col1 STRING, col2 FLOAT, col3 INT)")
    result_file = con.folder_path / "TEST_DATABASE" / "TEST_TABLE.csv"
    assert result_file.exists()       
    
    
@pytest.mark.parametrize("valid_query, expected_result", [
    ("SELECT * FROM TEST_DATABASE.TEST_TABLE WHERE col3 = 25", ("A", 2, 25)),
    ("SELECT col1, col2 + col3 AS col4 FROM TEST_DATABASE.TEST_TABLE", ("A", 27)),
    ("SELECT * FROM TEST_DATABASE.TEST_TABLE WHERE col2 + col3 = 13", ("A", 3, 10)),
    ("SELECT 1+2+3 AS E, 4*5-6 AS F", (6, 14)),
    ("SELECT * FROM TEST_DATABASE.TEST_TABLE", ("A", 2, 25)),
    ("SELECT col2 + col3, col2, col3, col3 * 2 FROM TEST_DATABASE.TEST_TABLE", (27, 2, 25, 50)),
    ("SELECT * FROM TEST_DATABASE.TEST_TABLE WHERE col2 >= 2 AND col3 <= 100", ("A", 2, 25))
])
def test_select_query_return_expect_result(con, valid_query, expected_result):
    result_file = con.folder_path / "TEST_DATABASE" / "TEST_TABLE.csv"
    # Add mock data
    with open(result_file, "a") as r:
        r.write("A, 2, 25 \r\n")
        r.write("A, 3, 10 \r\n")
    
    db_controller = DBController()
    query_id = db_controller.execute_query(con, valid_query)
    assert con.query_result[query_id]
    row_result = next(con.query_result[query_id]["result"])
    assert row_result == expected_result


@pytest.mark.parametrize("valid_query, expected_result", [
    ("SELECT * FROM TEST_DATABASE.TEST_TABLE WHERE col3 = 25", ("A", 2, 25)),
    ("SELECT col1, col2 + col3 AS col4 FROM TEST_DATABASE.TEST_TABLE", ("A", 27)),
    ("SELECT * FROM TEST_DATABASE.TEST_TABLE WHERE col2 + col3 = 13", ("A", 3, 10)),
    ("SELECT 1+2+3 AS E, 4*5-6 AS F", (6, 14)),
    ("SELECT * FROM TEST_DATABASE.TEST_TABLE", ("A", 2, 25)),
    ("SELECT col2 + col3, col2, col3, col3 * 2 FROM TEST_DATABASE.TEST_TABLE", (27, 2, 25, 50))
])
def test_call_next_data(con, valid_query, expected_result):
    result_file = con.folder_path / "TEST_DATABASE" / "TEST_TABLE.csv"
    # Add mock data
    with open(result_file, "a") as r:
        r.write("A, 2, 25 \r\n")
        r.write("A, 3, 10 \r\n")
    
    db_controller = DBController()
    query_id = db_controller.execute_query(con, valid_query)
    assert con.query_result[query_id]
    assert db_controller.fetch_next(con, query_id) == expected_result


def test_return_all_data_from_table(con):
    pass