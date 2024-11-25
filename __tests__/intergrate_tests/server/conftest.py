
import pytest
from dbcsv_server.connection import ConnectionIdentity
from dbcsv_server.transaction_manager import TransactionManager
from dbcsv_server.query_engine.parser import Parser
from functools import partial
from pathlib import Path

@pytest.fixture
def con():
    return ConnectionIdentity("test_data")
    
@pytest.fixture
def transaction_manager():
    return TransactionManager()

class MockQueryParser:
    
    @staticmethod
    def parse_select_clause():
        print("hello world")
        return None

@pytest.fixture
def mock_parser(request):
    query_parser = Parser(request.param)
    query_parser.parse_select_clause = MockQueryParser.parse_select_clause
    return query_parser


@pytest.fixture
def mock_task():
    def simple_task():
        return {
            "d": [1, 2, 4]
        }
    return partial(simple_task)

@pytest.fixture(scope="function")
def y(request):
    print(request)
    return request.param * 2

@pytest.fixture(scope="session")
def mock_create_table():
    
    def rm_rf(path):
        for item in path.iterdir():
            if item.is_dir():
                rm_rf(item)  # Recursively delete subdirectories
            else:
                item.unlink()  # Delete files
        path.rmdir()  # Remove the now-empty directory
    
    connection = ConnectionIdentity("test_data")
    Path.mkdir(connection.folder_path / "TEST_DATABASE")
    mock_file = connection.folder_path / "TEST_DATABASE" / "TEST_TABLE.csv"
    with open(mock_file, "w") as r:
        r.write("COL1,COL2,COL3\r\n")
        r.write("A,2,3\r\n")
        r.write("B,4,5")
    mock_meta_file = connection.folder_path / "TEST_DATABASE" / "meta.TEST_TABLE.csv"
    with open(mock_meta_file, "w") as r:
        r.write("column_name,column_type\r\n")
        r.write("COL1,STRING\r\n")
        r.write("COL2,INT\r\n")
        r.write("COL3,FLOAT\r\n")
    yield
    rm_rf(connection.folder_path)