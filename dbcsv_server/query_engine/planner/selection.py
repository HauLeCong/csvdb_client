from ..ast_node import PredicateNode
from typing import Iterator
from .production import Production
from .handler.predicate_handler import PredicateHandler

class Selection:
    
    def __init__(self, node: PredicateNode, source: Iterator[Production]):
        self.source = source
        self.data = None
        self.selection = node
        self.selection_handler = PredicateHandler(self)
      
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            self.data = next(self.source)
            row_result = self.selection_handler(self.selection)
            return row_result
        except StopIteration:
            raise 