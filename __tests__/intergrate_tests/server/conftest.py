
import pytest
from dbcsv_server.connection import ConnectionIdentity
from dbcsv_server.transaction_manager import TransactionManager
from functools import partial

@pytest.fixture
def con():
    return ConnectionIdentity("/test_data")
    
@pytest.fixture
def transaction_manager():
    return TransactionManager()

# class MockQueryExecutor:
    
#     def mock_task(self):
#         return {
#             "d": ["1", "2"]
#         }
  
#     def create_task(self):
#         return partial(self.mock_task)

# @pytest.fixture
# def mock_query_executor(monkeypatch):
    
#     def mock_create_task(*args, **kwargs):
#         return MockQueryExecutor.create_task
    
#     monkeypatch.setattr(QueryExecutor, "create_task", mock_create_task)

@pytest.fixture
def mock_task():
    def simple_task():
        return {
            "d": [1, 2, 4]
        }
    return partial(simple_task)