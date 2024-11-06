
import pytest
from dbcsv_server.transaction_manager import TransactionManager
from functools import partial
from dbcsv_server.connection import ConnectionIdentity

def test_init_transaction_manager():
    transaction_manager = TransactionManager()
    assert isinstance(transaction_manager, TransactionManager)
    
def test_return_query_id_add_task(con, transaction_manager, mock_task):
    """
        Test return query id on execute task
    """
    task = mock_task()
    query_id = transaction_manager.add_task_execute(con, task)
    assert query_id 

def test_add_task_closed_connection(con, transaction_manager, mock_task):
    """
        Test raise exception on closed connection
    """
    task = mock_task()
    assert con.closed == False
    con.close()
    assert con.closed == True
    with pytest.raises(SystemError) as e:
        assert transaction_manager.add_task_execute(con, task)

def test_run_task_success_add(con, transaction_manager):
    """
        Test add success task to task list
    """
    query_id = transaction_manager.add_task_execute(con, partial(lambda x: {"data": x}, ["1", "2", "3"]))
    print(query_id)
    task_list = transaction_manager.task_list
    print(transaction_manager.task_list)
    assert len(task_list.keys()) == 1
    assert next(iter(task_list.keys())) == query_id
    assert task_list[query_id]["status"] == "Success"

def test_run_task_fail_add(con, transaction_manager):
    """
        Test add fail task to task list
    """
    query_id = transaction_manager.add_task_execute(con, partial(lambda x: 1/0, ["1", "2", "3"]))
    task_list = transaction_manager.task_list
    assert len(task_list.keys()) == 1
    assert next(iter(task_list.keys())) == query_id
    assert task_list[query_id]["status"] == "Fail"
    assert task_list[query_id]["reason"] == "division by zero"

def test_ensure_task_complete_in_order(con, transaction_manager):
    """
        Test connection hold data after successful executed 
    """
    con = ConnectionIdentity("/test/data")
    transaction_manager = TransactionManager()
    query_id = transaction_manager.add_task_execute(con, partial(lambda x: {"data": x}, 1))
    assert next(iter(con.query_result.keys())) == query_id
    assert con.query_result[query_id]["result"]
    
    


