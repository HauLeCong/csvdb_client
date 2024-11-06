from dbcsv_server.connection import ConnectionIdentity
from pathlib import Path
import pytest

def test_object_create_on_connection():
    """
        Test create connection entity
    """
    path = Path("test/data")
    con = ConnectionIdentity(path)
    assert con.closed == False
    
@pytest.mark.parametrize("url", [(1, ), (True, ), (None, )])
def test_povide_invalid_path_folder(url):
    """
        Test give invalid folder_path
    """
    with pytest.raises(TypeError) as e:
        assert ConnectionIdentity(url)
    assert e.value.args[0] == "Folder path must be string or Path" 

@pytest.mark.parametrize("url", ["test", "test/data", "test/data/sub"])
def test_create_folder_on_connection(url):
    con = ConnectionIdentity("test/data")
    assert Path.exists(con.folder_path)


    