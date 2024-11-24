from ..ast_node import (
    ColumnListNode
)

from typing import Iterator
from .handler.column_list_handler import ColumnListHandler

class Projection:
    
    """
        This class is mimic Project relatinal algebra
    """
    
    def __init__(self, node: ColumnListNode, source: Iterator):
        self.projection = node
        self.source = source
        self.data = None
        self.projection_hanlder = ColumnListHandler(self)
        
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            self.data = next(self.source)
            row_result = self.projection_hanlder.call_handler(self.projection)
            return row_result
        except StopIteration:
            raise 