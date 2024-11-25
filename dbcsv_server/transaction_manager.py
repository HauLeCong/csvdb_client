from .connection import ConnectionIdentity
from datetime import datetime, timezone
from typing import Dict, Iterator

class DataResult:  
    def __init__(self, data: Iterator):
        self.data = data
        self.current_row = None
        self.current_row_return = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            self.current_row = next(self.data)
            if len(self.current_row["data"]) > 0:
                self.current_row_return += 1
                self.description = self.current_row["columns"]
                return self.current_row["data"]
            return self.__next__()
        except StopIteration:
            if self.current_row_return == 0:
                return ()
            raise(f"Stop iteration")
        
class TransactionManager:
    """
    A class to handle query executor result and query
    """

    def __init__(self):
        self._task_list: Dict[str, dict] = {}
        
    @property
    def task_list(self) -> dict:
        return self._task_list
    
    def add_task_execute(self, con: ConnectionIdentity, task, task_type) -> str:
        if con.closed == True:
            raise SystemError("Cannot operate on closed connection")
        try:
            query_id = datetime.now(tz=timezone.utc).strftime("%d%m%Y%H%M%S")
            result = task()
            self._task_list.update({query_id: {"status": "Success"}}) 
            if task_type == "query":
                con.query_result.update({query_id: {"result": DataResult(result)}})
            elif task_type == "create":
                con.query_result.update({query_id: {"result": iter()}})
        except Exception as e:
            self._task_list.update({query_id: {"status": "Fail", "reason": e.args[0]}})
            raise 
        finally:
            return query_id

    def cancel(self, con: ConnectionIdentity, query_id: str):
        pass

