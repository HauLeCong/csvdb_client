import pytest


def test_connect_successful(mock_client):
    connect_respnse = mock_client.get("http://127.0.0.1:8000/connect")
    assert connect_respnse.status_code == 200
    import json
    data = json.loads(connect_respnse.content.decode())
    assert data["connection_id"]
    
def test_query_successful(mock_client):
    import json
    connect_res = mock_client.get("http://127.0.0.1:8000/connect")
    connect_id = json.loads(connect_res.content.decode())["connection_id"]
    create_tab_res = mock_client.post("http://127.0.0.1:8000/query", json={"connection_id": connect_id, "query": "CREATE TABLE TEST_DATABASE.TEST_DATA (COL1 STRING, COL2 STRING)"})
    query_id = json.loads(create_tab_res.content.decode())["query_id"]
    print("***QUERYID", query_id)
    assert query_id
    select_res = mock_client.post("http://127.0.0.1:8000/query", json={"connection_id": connect_id, "query": "SELECT * FROM TEST_DATABASE.TEST_DATA"})
    query_id = json.loads(select_res.content.decode())["query_id"]
    assert query_id
    fetch_res = mock_client.post("http://127.0.0.1:8000/fetch", json={"connection_id": connect_id, "query_id": query_id})
    fetch_data = json.loads(fetch_res.content.decode())
    assert fetch_data["description"] == None
    
def test_return_400_when_provide_close_connect():
    pass

def test_return_400_when_not_provide_qeury():
    pass

def test_return_400_when_not_provide_connection_id():
    pass