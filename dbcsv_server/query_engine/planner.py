
from .ast_node import SelectNode, FromNode, WhereNode, PredicateNode, PredicateOrNode, ColumnListNode
from functools import partial
from typing import Any, Iterator
from functools import partial

class QueryPlanner:
    """
        This class convert a AST to plan of relational algebra

    """
    
    def __init__(self):
        pass
    
    def visit(self, node: Any, *args, **kwargs):
        pass
    
    def get_node_handler(self, node_type: str):
        pass
    
    def handle_select_clause(self, node: SelectNode):
        from_iterator = self.visit(node.from_clause)
        where_iterator = self.visit(node.where_clause, from_iterator)
        select_iterator = map(partial(self.visit, node.select_clause), where_iterator)
        
    def handle_from_clause(self, node: FromNode):
        #return List|csv lib to yield record
        pass

    def handle_where_clause(self, node: WhereNode, from_values: Iterator):
        
        result = filter(lambda x: self.visit(node.predicate, x), from_values)
        return 
    
    def handle_predicate_node(self, node: PredicateNode, row: dict):
        pass
    
    def handle_column_list_node(self, node: ColumnListNode, row: dict):
        result = {}
        
        
        #and or
        
        # function input function and return function
        # iterator
        # map_filter
        # FROM -> iterator
        # WHERE -> iterator
        # SELECT -> iterator
        # Append with executor 
        
        SELECT(WHERE(FROM()))
    