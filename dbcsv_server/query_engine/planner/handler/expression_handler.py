
from operator import *

from .base_handler import BaseHandler
from ...ast_node import (
        ExprNode,
        ExprAddNode,
        ExprMultiNode,
        ExprValueNode,
        ExprParentNode,
        ValueNode
    )
from ...token import Token, ReservedWord

ops = {
    Token.PLUS: add,
    Token.MINUS: sub,
    Token.ASTERISK: mul,
    Token.DIVIDE: truediv,
}
class ExpressionHandler(BaseHandler):
    
    def __init__(self, caller):
        super().__init__(caller)
        if not self._caller._data:
            raise RuntimeError(f"Data not found")
        self._data = self._caller._data
       
    def get_node_handler(self, node_type: str):
        match node_type:
            case "ExprAdd":
                return self.handle_expression_add_node
            case "ExprMulti":
                return self.handle_expression_multi_node
            case "ExprValue":
                return self.handle_expression_value_node
            case "Value":
                return self.handle_value_node
            case "ExprParent":
                return self.handle_expression_parent_node 
    
    def call_handler(self, node, *args, **kwargs):
        handler = self.get_node_handler(node.type)
        return handler(node, *args, **kwargs)       
            
    def handle(self, node: ExprNode):
        if not isinstance(node, ExprNode):
            raise ValueError(f"Expected an expression got {self.node.__class__.__name__}")
        return self.handle_expression_add_node(node.expr)
        
    def handle_expression_add_node(self, expr_add_node: ExprAddNode):
        left_value = self.call_handler(expr_add_node.left)
        if expr_add_node.right:
            right_value = self.call_handler(expr_add_node.right)
            return ops[expr_add_node.operator](left_value, right_value)
        return left_value
    
    def handle_expression_multi_node(self, expr_multi_node: ExprMultiNode):
        left_value = self.call_handler(expr_multi_node.left)
        if expr_multi_node.right:
            right_value = self.call_handler(expr_multi_node.right)
            return ops[expr_multi_node.operator](left_value, right_value)
        return left_value

    def handle_expression_value_node(self, expr_value_node: ExprValueNode):
        if isinstance(expr_value_node.expr, ValueNode):
            return self.call_handler(expr_value_node.expr)
        return expr_value_node.expr[1]
        
    def handle_value_node(self, value_node: ValueNode):
        if isinstance(value_node.expr, ExprParentNode):
            return self.call_handler(value_node.expr)
        try:
            return self._data[value_node.expr[1]]
        except KeyError:
            raise RuntimeError(f"Column {value_node.expr[1]} not found")
    
    def handle_expression_parent_node(self, expr_parent_node: ExprParentNode):
        return self.call_handler(expr_parent_node.expr)