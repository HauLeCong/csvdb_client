
from dbcsv_server.connection import ConnectionIdentity
from dbcsv_server.db_controller import DBController
import pytest
from pathlib import Path
import pandas as pd


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
    
    def rm_rf(path):
        for item in path.iterdir():
            if item.is_dir():
                rm_rf(item)  # Recursively delete subdirectories
            else:
                item.unlink()  # Delete files
        path.rmdir()  
    
    assert result_file.exists()   
    rm_rf(con.folder_path)    
    
@pytest.mark.parametrize("valid_query, expected_result", [
    ("SELECT * FROM TEST_DATABASE.TEST_TABLE WHERE col3 = 3", ("A", 2, 3)),
    ("SELECT col1, col2 + col3 AS col4 FROM TEST_DATABASE.TEST_TABLE", ("A", 5)),
    ("SELECT * FROM TEST_DATABASE.TEST_TABLE WHERE col2 + col3 = 5", ("A", 2, 3)),
    ("SELECT 1+2+3 AS E, 4*5-6 AS F", (6, 14)),
    ("SELECT * FROM TEST_DATABASE.TEST_TABLE", ("A", 2, 3)),
    ("SELECT col2 + col3, col2, col3, col3 * 2 FROM TEST_DATABASE.TEST_TABLE", (5, 2, 3, 6)),
    ("SELECT * FROM TEST_DATABASE.TEST_TABLE WHERE col2 >= 2 AND col3 <= 100", ("A", 2, 3)),
    ("SELECT 'b', 'c', 'd'", ("B", "C", "D"))
])
def test_select_query_return_expect_result(con, valid_query, expected_result, mock_create_table):
    """
    Test first result return is equal to the expected result
    """
    db_controller = DBController()
    query_id = db_controller.execute_query(con, valid_query)
    assert con.query_result[query_id]
    row_result = next(con.query_result[query_id]["result"])
    assert row_result == expected_result

@pytest.mark.parametrize("valid_query", ["SELECT * FROM TEST_DATABASE.TEST_TABLE"])
def test_return_all_data_from_table(con, valid_query, mock_create_table):
    """
    Test that all rows returns
    """
    
    db_controller = DBController()
    query_id = db_controller.execute_query(con, valid_query)
    df = pd.read_csv(con.folder_path / "TEST_DATABASE" / f"TEST_TABLE.csv")
    row_counts = 0
    for i, row in df.iterrows():
        assert tuple(row) == next(con.query_result[query_id]["result"])
        row_counts += 1
        
    assert df.shape[0] == row_counts
    
@pytest.mark.parametrize("valid_query", ["SELECT * FROM TEST_DATABASE.TEST_TABLE WHERE col2 = 2 AND (col1 = 'A' OR col3 < 25)"])
def test_complex_where_clause(con, valid_query, mock_create_table):
    db_controller = DBController()
    query_id = db_controller.execute_query(con, valid_query)
    df = pd.read_csv(con.folder_path / "TEST_DATABASE" / f"TEST_TABLE.csv")
    filter_col2 = df["COL2"] == 2
    filter_col1 = df["COL1"] == 'A'
    filter_col3 = df["COL3"] < 25
    df = df[filter_col2 & (filter_col1 | filter_col3)]
    print("****", df)
    count_rows = 0
    for i, row in df.iterrows():
        assert tuple(row) == next(con.query_result[query_id]["result"])
        count_rows += 1
        
    assert count_rows == df.shape[0]