from collections.abc import Iterator, Iterable
from typing import LiteralString, Self, List, Tuple
import requests

class Cursor(Iterator):
    def __init__(self, connection, description: Tuple[tuple] = None) -> None:
        self.description = description
        self.connection = connection
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, metadata):
        self._description = metadata
    
    def callproc(self):
        pass
    
    def close(self):
        pass
    
    def _prepare_query_param(self, params: Iterable):
        pass
    
    def execute(self, sql: LiteralString, parameters: Iterable = None) -> Self:
        if not isinstance(sql, str):
            raise TypeError("Query must be a string")
        
        if parameters and not isinstance(parameters, Iterable):
            raise ValueError("Parameters must be interable: tuple, list or Row")
        # Prepare parameter
        # Execute query -> get result
        # Map column to description
        return True
        
    def executemany(self, sql: LiteralString, parameters: Iterable[str] = None) -> Self:
        pass
    
    def fetchone(self):
        pass
    
    def fetchmany(self):
        pass
    
    def fetchall(self):
        pass
    
    def nextset(self):
        pass
    
    def arraysize(self):
        pass
    
    def setinputsizes(self, sizes):
        pass
    
    def setoutputsizes(self, sizes):
        pass
    
    def __iter__(self) -> Self:
        return self
    
    def __next__(self):
        pass
    