
import pytest
from dbcsv_server.connection import ConnectionIdentity
from dbcsv_server.transaction_manager import TransactionManager
from dbcsv_server.query_engine.parser import QueryParser
from functools import partial

@pytest.fixture
def con():
    return ConnectionIdentity("/test_data")
    
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
    query_parser = QueryParser(request.param)
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