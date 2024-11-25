from ..ast_node import (
    ColumnListNode
)

from typing import Iterator
from .handler.column_list_handler import ColumnListHandler

class Projection:
    
    """
        This class is mimic Project relatinal algebra
    """
    
    def __init__(self, node: ColumnListNode, source: Iterator = None):
        self.projection = node
        self.source = source
        self.data = None
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if not self.source:
            self.data = None
            projection_handler = ColumnListHandler(self)
            row_result = projection_handler.handle(self.projection)
            return row_result
        try:
            current_row = next(self.source) 
            self.data = current_row["data"] 
            current_predicate = current_row["predicate"]
            projection_handler = ColumnListHandler(self)
            row_result = projection_handler.handle(self.projection)
            if current_predicate:
                return row_result
            else:
                row_result["data"] = ()
                return row_result
        except StopIteration:
            raise 
    
    def __call__(self):
        return self.__next__()