

from .base_handler import BaseHandler
from ...ast_node import ( 
    PredicateNode, 
    PredicateOrNode, 
    PredicateAndNode, 
    PredicateNotNode, 
    PredicateCompareNode,
    PredicateParentNode, 
    ExprNode
)
from ...token import Token, ReservedWord

from operator import *

ops = {
    Token.LESS_THAN: lt,
    Token.GREATER_THAN: gt,
    Token.LESS_THAN_EQUAL: le,
    Token.GREATER_THAN_EQUAL: ge,
    Token.EQUAL: eq,
    ReservedWord.OR: or_,
    ReservedWord.AND: and_,
    ReservedWord.NOT: not_
}

class PredicateHandler(BaseHandler):
    
    def __init__(self, caller):
        super().__init__(caller)
        if not self._caller.data:
            raise RuntimeError(f"Data not found")
        self._data = self._caller.data
        
    def get_node_handler(self, node_type: str):
        match node_type:
            case "Predicate":
                return self.handle
            case "PredicateOr":
                return self.handle_predicate_or_node
            case "PredicateAnd":
                return self.handle_predicate_and_node
            case "PredicateNot":
                return self.handle_predicate_not_node
            case "PredicateCompare":
                return self.handle_predicate_compare_node
            case "PredicateParent":
                return self.handle_predicate_parent_node
            case _:
                raise RuntimeError(f"Unexpected node {node_type}")
            
    def call_handler(self, node, *args, **kwargs) -> bool:
        handler = self.get_node_handler(node.type)
        return handler(node, *args, **kwargs)
        
    def handle(self, node: PredicateNode):
        if not isinstance(node, PredicateNode):
            raise ValueError(f"Expected a predicate got {node.__class__.__name__}")
        return self.call_handler(node.expr)
    
    def handle_predicate_or_node(self, node: PredicateOrNode):
        left_value = self.call_handler(node.left)
        if node.right:
            right_value = self.call_handler(node.right)
            return ops[node.operator](left_value, right_value)
        return left_value
    
    def handle_predicate_and_node(self, node: PredicateAndNode):
        left_value = self.call_handler(node.left)
        if node.right:
            right_value = self.call_handler(node.right)
            return ops[node.operator](left_value, right_value)
        return left_value
    
    def handle_predicate_not_node(self, node: PredicateNotNode):    
        if node.operator:
            return ops[node.operator](self.call_handler(node.expr))
        return self.call_handler(node.expr)
    
    def handle_predicate_compare_node(self, node: PredicateCompareNode) -> bool:
        if isinstance(node.left, PredicateParentNode):
            return self.call_handler(node.left)

        from .expression_handler import ExpressionHandler
        expression_handler = ExpressionHandler(self)
        left_value = expression_handler.handle(node.left)
        if node.right:
            right_value = expression_handler.handle(node.right)
            return ops[node.operator](left_value, right_value)
        return left_value
        
    def handle_predicate_parent_node(self, node: PredicateParentNode):
        return self.call_handler(node.expr)