from ..ast_node import PredicateNode
from typing import Iterator
from .production import Production
from .handler.predicate_handler import PredicateHandler

class Selection:
    
    def __init__(self, source: Iterator[Production], node: PredicateNode = None):
        self.source = source
        self.selection = node
        self.data = None
      
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            self.data = next(self.source)
            if self.selection:
                predicate_handler = PredicateHandler(self)
                predicate = predicate_handler.handle(self.selection)
                return {"data": self.data, "predicate":  predicate}
            return {"data": self.data, "predicate": True}
        except StopIteration:
            raise 