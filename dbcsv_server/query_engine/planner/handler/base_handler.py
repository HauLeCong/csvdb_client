
from abc import ABC, abstractmethod


class BaseHandler(ABC):
    def __init__(self, caller):
        self._caller = caller
        
    @abstractmethod
    def handle(self, node):
        raise NotImplementedError(f"Must implement {self.handle.__name__}")
    
    @abstractmethod
    def call_handler(self, node, *args, **kwargs):
        raise NotImplementedError(f"Must implement {self.call_handler.__name__}")
    
    @abstractmethod
    def get_node_handler(self, node_type: str):
        raise NotImplementedError(f"Must implement {self.get_node_handler.__name__}")