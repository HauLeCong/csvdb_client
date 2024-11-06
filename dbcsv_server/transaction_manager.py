from .connection import ConnectionIdentity
from datetime import datetime, timezone
from typing import Dict, Iterable

class DataResult:  
    def __init__(self, data: Iterable):
        self.data = data
        self.current_row = 0
        self.current_data = None
        self.total_line = len(data)
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current_row < self.total_line:
            self.current_data = self.data[self.current_row]
            self.current_row += 1
            return self.current_data
        else:
            raise StopIteration

class TransactionManager:
    """
    A class to handle query executor result and query
    """

    def __init__(self):
        self._task_list: Dict[str, dict] = {}
        
    @property
    def task_list(self) -> dict:
        return self._task_list
    
    def add_task_execute(self, con: ConnectionIdentity, task) -> str:
        if con.closed == True:
            raise SystemError("Cannot operate on closed connection")
        try:
            query_id = datetime.now(tz=timezone.utc).strftime("%d%m%Y%H%M%S")
            result = task()
            self._task_list.update({query_id: {"status": "Success"}}) 
            con.query_result.update({query_id: {"result": DataResult(result)}})
        except Exception as e:
            self._task_list.update({query_id: {"status": "Fail", "reason": e.args[0]}})
            raise 
        finally:
            return query_id

    def cancel(self, con: ConnectionIdentity, query_id: str):
        pass

