from ..ast_node import (
    ColumnListNode,
    ColumnNode,
    ColumnWildCardNode,
    ExprNode, 
    ExprAddNode, 
    ExprMultiNode, 
    ExprValueNode, 
    ValueNode, 
    ExprParentNode
)


from ..token import Token, ReservedWord
from operator import add, sub, mul, truediv, lt, gt, le, ge, or_, and_, xor, not_
from typing import List, Dict



class Projection:
    
    """
        This class is mimic Project relatinal algebra
    """
    
    def __init__(self, projection: ColumnListNode, source: List[Dict]):
        self.projection = projection
        self.source = source
        
    
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            row_result = self.get_node_handler(self.projection, next(self.source))
            return row_result
        except StopIteration:
            raise 