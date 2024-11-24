
from functools import partial
from typing import Any, Iterator
import operator
from functools import partial


from ..ast_node import (
        SelectNode, 
        FromNode, 
        WhereNode, 
        PredicateNode, 
        PredicateCompareNode,
        ColumnListNode,
        ExprNode,
        ExprAddNode,
        ExprMultiNode,
        ExprValueNode,
        ExprParentNode,
        ValueNode
    )

from .selection import Selection
from .projection import Projection
from .production import Production

class QueryPlanner:
    """
        This class convert a AST to plan of relational algebra

    """
    
    def __init__(self):
        pass
    
    def visit(self, node: Any, *args, **kwargs):
        print("He*****llo" , node)
        handler = self.get_node_handler(node.type)
        return handler(node, *args, **kwargs)
    
    def get_node_handler(self, node_type: str):
        match node_type:
            case "ExprValue":
                return self.handle_expr_value_node
            case "Value":
                return self.handle_value_node
            case "ExprParent":
                return self.handle_expr_parent_node
    
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
        
    
    def handle_predicate_compare_node(self, node: PredicateCompareNode):
        pass
    
    def handle_expr_multi_node(self, node: ExprMultiNode):
        left = self.visit(node.left)
        if node.right:
            right = self.visit(node.right)
            
    def handle_expr_value_node(self, node: ExprValueNode, data):
        if isinstance(node.expr, ValueNode):
            return partial(lambda x: x, self.visit(node.expr)())
        return partial(lambda x: x, node.expr[1])
    
    def handle_value_node(self, node: ValueNode, data) -> partial:
        if isinstance(node.expr, ExprParentNode):
            return partial(lambda x: x, self.visit(node.expr, data)())
        return partial(lambda x: x, node.expr)
    
    def handle_expr_parent_node(self, node: ExprParentNode, data) -> partial:
        return self.visit()
    
            
        #and or
        
        # function input function and return function
        # iterator
        # map_filter
        # FROM -> iterator
        # WHERE -> iterator
        # SELECT -> iterator
        # Append with executor 
        
        # SELECT(WHERE(FROM()))
    