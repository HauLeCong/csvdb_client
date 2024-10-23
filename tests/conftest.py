import pytest
import dbapi2
import time

@pytest.fixture()
def mock_path_file(scope="module"):
    return "../util_folder/"

@pytest.fixture(scope="module")
def mock_insert_data_list():
    return [()]

@pytest.fixture(scope="module")
def mock_data_id():
    return 1

@pytest.fixture(scope="module")
def mock_insert_data(mock_data_id):
    #id, col1, col2
    return (mock_data_id, "", "")

@pytest.fixture(scope="function")
def dbapi2_connections(mock_path_file):
    try:
        conn = dbapi2.connect(mock_path_file)
        conn2 = dbapi2.connect(mock_path_file)
        yield conn, conn2
    except Exception as e:
        print(e)
    finally:
        conn.close()
        
@pytest.fixture(autouse=True)
def log_execution_time():
    start_time = time.time()
    yield 
    delta = time.time() - start_time
    print("\n test duration: {:0.3} seconds".format(delta))