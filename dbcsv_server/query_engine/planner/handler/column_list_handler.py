from typing import Any, Dict

from .base_handler import BaseHandler
from ..projection import Projection
from ...ast_node import ColumnListNode, ColumnWildCardNode, ColumnNode


class ColumnListHandler(BaseHandler):
    
    def __init__(self, caller):
        super().__init__(caller)
        if not self._caller._data:
            raise RuntimeError(f"Data not found")
        self._data = self._caller._data
        self.holding_left = None
        
    def get_node_handler(self, node_type: str):
        match node_type:
            case "ColumnList":
                return self.handle
            case "Column":
                return self.handle_column_node
    
    def call_handler(self, node, *args, **kwargs):
        handler = self.get_node_handler(node.type)
        return handler(node, *args, **kwargs)
        
    def handle(self, node: ColumnListNode) -> Any:
        """
        This return a projection row which is a dict with value and keys
        Args:
            node (ColumnListNode): _description_
            data (Dict): a dict of data {"key": value}
        Returns:
            Dict: return a dict which seperate key from value make sure that key, value have same number of elements
        """
        
        left_result = self.call_handler(node.left)
        left_keys, left_values = tuple(left_result.keys()), tuple(left_result.values())
        if node.right:
            right_result = self.call_handler(node.right)
            right_keys, right_values = tuple(right_result.keys()), tuple(right_result.values())
            return dict(columns=left_keys+right_keys, data=left_values+right_values)
        return dict(columns=left_keys, data=left_values)
            
    def handle_column_node(self, node: ColumnNode) -> Dict:
        if isinstance(node.expr, ColumnWildCardNode):
            return self._data
        from .expression_handler import ExpressionHandler
        expr_handler = ExpressionHandler(self)
        expr_value = expr_handler.handle(node.expr)
        return {f"{node.name}": expr_value} if not node.alias else {f"{node.alias}": expr_value}
        
        
    

    
    