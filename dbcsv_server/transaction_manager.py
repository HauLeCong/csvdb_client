from .connection import ConnectionIdentity
from datetime import datetime, timezone
from typing import Dict, Iterator

class DataResult:  
    """
        Result wraper for query result
    """
    def __init__(self, data: Iterator):
        self.data = data
        self.current_row = None
        self.current_row_return = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        """
        Return data row by row, if a row is blank skip to next 
        if still nothing return a blank tuple then StopIteration on the next round
        Returns:
            description: a tuple of columns for client
            result_row: a result row of query data
        """
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
    A class to handle result and return query id
    """

    def __init__(self):
        self._task_list: Dict[str, dict] = {}
        
    @property
    def task_list(self) -> dict:
        """To keep track of all tasks that executed"""
        return self._task_list
    
    def add_task_execute(self, con: ConnectionIdentity, task, task_type) -> str:
        """
            Add task to task list and executed, if succeed return query id
        
        """
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

