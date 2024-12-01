from .query_engine.parser import Parser
from .connection import ConnectionIdentity
from .transaction_manager import TransactionManager
from .query_engine.planner import Selection, Production, Projection, TableCreation
from .query_engine.ast_node import SelectNode, CreateTableNode
from .data_storage import FileManager
from typing import TypedDict
from functools import partial


class FetchedData(TypedDict):
    data: tuple
    description: tuple


class DBController:
    """
    This class act as the interface for database
    """

    def __init__(self):
        self.transaction_manager = TransactionManager()
        self._con_list = {}

    def connect(self) -> ConnectionIdentity:
        """
        Generate a connection object
        Returns:
            ConnectionIdentity
        """
        con = ConnectionIdentity()
        self._con_list.update({f"{con.id}": con})
        return con

    def disconnect(self, con_id: str):
        """
        Close a connection
        Args:
            con (ConnectionIdentity):
        """
        con = self._con_list.get(con_id)
        con.close()
        self._con_list.pop(con_id)

    def execute_query(self, con_id: str, sql_str: str) -> str:
        """
        Execute a sql string
        Args:
            con (ConnectionIdentity)
            sql_str (str):
        Returns:
            query_id (str): a query id point to result of the query, it is not guarantee that the query is execute successful or not
        """
        con = self._con_list.get(con_id)
        if not con or con.closed == True:
            raise SystemError("Fail to get connection or connection closed")
        try:
            query_parser = Parser(sql_str)
            ast = query_parser.parse()
            file_manager = FileManager()
            # ***Need to implement: add an abstract class to handle all node

            #
            if isinstance(ast.nodes, SelectNode):
                if ast.nodes.from_clause:
                    production = Production(
                        ast.nodes.from_clause,
                        partial(file_manager.select_file, con=con),
                    )
                    if ast.nodes.where_clause:
                        selection = Selection(
                            node=ast.nodes.where_clause.expr, source=production
                        )
                        plan = partial(Projection, ast.nodes.column_list, selection)
                        query_id = self.transaction_manager.add_task_execute(
                            con, plan, "query"
                        )
                    else:
                        selection = Selection(node=None, source=production)
                        plan = partial(Projection, ast.nodes.column_list, selection)
                        query_id = self.transaction_manager.add_task_execute(
                            con, plan, "query"
                        )
                else:
                    plan = partial(Projection, node=ast.nodes.column_list, source=None)
                    query_id = self.transaction_manager.add_task_execute(
                        con, plan, "query"
                    )
            elif isinstance(ast.nodes, CreateTableNode):
                table_creation = TableCreation(ast.nodes)
                plan = partial(
                    file_manager.create_table_file,
                    con,
                    table_creation.create_database,
                    table_creation.create_table_name,
                    table_creation.create_column_list,
                )
                query_id = self.transaction_manager.add_task_execute(
                    con, plan, "create"
                )
            else:
                raise ValueError(f"Not support query: {sql_str}")
        except Exception as e:
            raise
        return query_id

    def fetch_result(self, con_id: str, query_id: str, num_record: int) -> FetchedData:
        """
        Return a next row of a query result
        Args:
            con (ConnectionIdentity)
            query_id (str)

        Returns:
            Dict:
        """
        con = self._con_list.get(con_id)
        try:
            return {
                "data": next(con.query_result[query_id]["result"]),
                "description": (con.query_result[query_id]["result"]).description,
            }
        except Exception as e:
            raise
