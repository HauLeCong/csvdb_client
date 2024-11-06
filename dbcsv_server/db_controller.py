from .query_engine import QueryParser, QueryPlanner, ExecutionPlan
from .connection import ConnectionIdentity
from .query_executor import QueryExecutor
from .transaction_manager import TransactionManager
from typing import Dict

class DBController:
    """
        This class act as the interface for database
    """
    def __init__(self):
        self.transaction_manager = TransactionManager()

    def connect(self) -> ConnectionIdentity:
        """
        Generate a connection object
        Returns:
            ConnectionIdentity
        """
        con = ConnectionIdentity()
        return con
    
    def disconnect(self, con: ConnectionIdentity):
        """
        Close a connection
        Args:
            con (ConnectionIdentity):
        """
        con.delete()
        
    def execute_query(self, con: ConnectionIdentity, sql_str: str) -> str:
        """
        Execute a sql string
        Args:
            con (ConnectionIdentity)
            sql_str (str):
        Returns:
            query_id (str): a query id point to result of the query, it is not guarantee that the query is execute successful or not
        """
        if con.closed == True:
            raise SystemError("Cannot operate on closed connection")
        try:
            query_parser = QueryParser()
            ast = query_parser.parse(sql_str)
            query_planner = QueryPlanner()
            plan = query_planner.build(ast)
            query_executor = QueryExecutor()
            execute_task = query_executor.create_task(con, plan)
            query_id = self.transaction_manager.add_task_execute(con, execute_task)
        except Exception as e:
            raise
        return query_id
    
    def fetch_next(self, con: ConnectionIdentity, query_id: str) -> Dict:
        """
        Return a next row of a query result
        Args:
            con (ConnectionIdentity)
            query_id (str)

        Returns:
            Dict: 
        """
        try:
            return next(con.query_result[query_id]["result"])
        except Exception as e:
            raise        

        
        
    