from typing import Any, Dict

from .base_handler import BaseHandler
from ...ast_node import ColumnListNode, ColumnWildCardNode, ColumnNode


class ColumnListHandler(BaseHandler):
    
    def __init__(self, caller):
        super().__init__(caller)
        self.holding_right = []
        self.holding_left = []
        
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
        left_value = None
        if isinstance(node.left, ColumnListNode):
            self.call_handler(node.left)
            if node.right:
                right_value = self.call_handler(node.right)
                self.holding_right.append(right_value)
        else:
            left_value = self.call_handler(node.left)
            self.holding_left.append(left_value)
        left_keys = tuple([k for i in self.holding_left for k in i.keys()])
        right_keys = tuple([k for i in self.holding_right for k in i.keys()])
        left_values = tuple([k for i in self.holding_left for k in i.values()])
        right_values = tuple([k for i in self.holding_right for k in i.values()])
        return dict(columns = left_keys + right_keys, data = left_values + right_values) 
    
    def handle_column_node(self, node: ColumnNode) -> Dict:
        if isinstance(node.expr, ColumnWildCardNode):
            return self._caller.data
        from .expression_handler import ExpressionHandler
        expr_handler = ExpressionHandler(self._caller)
        expr_value = expr_handler.handle(node.expr)
        return {f"{node.name}": expr_value} if not node.alias else {f"{node.alias[1]}": expr_value}
    
    def handle_column_name_wo_data(self, node: ColumnNode) -> Dict:
        if isinstance(node.expr, ColumnWildCardNode):
            return {f"{node.name}"}
        
        
    

    
    