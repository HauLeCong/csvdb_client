from .query_engine import ExecutionPlan
from .connection import ConnectionIdentity
from .query_engine import QueryPlanner
from .data_storage import FileManager
from functools import partial
from typing import Dict

class QueryExecutor:
    """
        Convert sql query plan to normal IO python function
        - select(): sql select operation
        - create(): sql create table operation
        - where(): sql where operation
        - execute(): combine all sql operation
    """
    def __init__(self):
        self.file_manager= FileManager()
    
    def create_task(self, con: ConnectionIdentity, plan: ExecutionPlan) -> partial:
        if con.closed == True:
            raise SystemError("Cannot operate on closed connection")
        return partial(self.execute, plan)
    
    def execute(self, con: ConnectionIdentity, plan: QueryPlanner) -> Dict|None:
        pass
    
    def select(self):
        self.file_manager.select_file()
    
    def create(self):
        self.file_manager.create_file()
    
    def where(self):  
        pass
    
