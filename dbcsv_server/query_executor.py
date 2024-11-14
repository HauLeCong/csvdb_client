from .query_engine.parser import ExecutionPlan
from .connection import ConnectionIdentity
from .query_engine.parser import QueryPlanner
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
    
    def get_handler(self, node_type):
        if node_type == "Arimethic":
            return self.handle_arimethic_node
        elif node_type == "Factor":
            return self.handle_factor_node
        elif node_type == "Term":
            return self.handle_term_node
        elif node_type == "Logical":
            return self.handle_logical_node
    
    def visit(self, node):
        handler = self.get_handler(node.type)
        return handler(node)
        
    def handle_logical_node(self, logical_node):
        #left, right, operator
        left_value = self.visit(logical_node.left)
        right_value = self.visit(logical_node.right)
        if logical_node.operator == "AND":
            return left_value and right_value
        
    def handle_arimethic_node(self, arimethic_node):
        print(arimethic_node)
        left_value = self.visit(arimethic_node.left)
        if arimethic_node.right:
            right_value = self.visit(arimethic_node.right)
            if arimethic_node.operator.value == '+':
                return left_value + right_value 
            elif arimethic_node.operator.value == "-":
                return left_value - right_value
        return left_value
        
    def handle_term_node(self, term_node):
        left_value = self.visit(term_node.left)
        if term_node.right:
            right_value = self.visit(term_node.right)
            if term_node.operator.value == "*":
                return left_value * right_value
            elif term_node.operator.value == "/":
                return left_value / right_value
        return left_value
    
    def handle_factor_node(self, factor_node):
        if not hasattr(factor_node.expr, "left"):
            return factor_node.expr
        return self.visit(factor_node.expr)
    
    def handle_ast_node(self, ast_node):
        return self.visit(ast_node.expr)
    
    def handle_from_node(self, from_node):
        table_name = from_node
        data = self.select(table_name)
        return data
    
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
    
