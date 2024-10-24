from dbapi2 import Cursor
from typing import LiteralString, Tuple, List, override

class MockCursor(Cursor):
    
    def __init__(self, description = None):
        super().__init__(description)
        
    @override
    def execute(self, sql, parameters):
        pass
    
    @override
    def executemany(self, sql, parameters):
        pass
    
    