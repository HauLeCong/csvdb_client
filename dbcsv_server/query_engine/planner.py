
from .ast_node import AST

class QueryPlanner:
    """
        This class convert a AST to plan of AST nodes
    """
    
    def __init__(self):
        pass
        
    def build(self, ast: AST) -> 'ExecutionPlan':
        pass
    
class ExecutionPlan:
    
    def __init__(self, nodes: List["ExecutionNode"]):
        pass
    

class ExecutionNode:
    pass