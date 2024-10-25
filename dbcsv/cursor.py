from collections.abc import Iterator, Iterable
from typing import LiteralString, Self, List, Tuple
from .exceptions import ProgramingError
import requests

class Cursor(Iterator):
    def __init__(self, connection) -> None:
        self.connection = connection
        self.arraysize = 1
        self.description = None
        self._closed = 0
        self._current_row = None
        self._data = None

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, metadata):
        self._description = metadata
        
    @property
    def arraysize(self):
        return self._arraysize
        
    @arraysize.setter
    def arraysize(self, size: int):
        if not isinstance(size, int):
            raise TypeError("Arraysize must be an integer")
        self._arraysize = size
        
    def callproc(self):
        pass
    
    def close(self):
        self._closed = 1
    
    def _prepare_query_param(self, params: Iterable):
        pass
    
    def execute(self, sql: LiteralString, parameters: Iterable = None) -> Self:
        if self._closed == 1:
            raise ProgramingError("Cannot operate on a closed cursor.")
            
        if not isinstance(sql, str):
            raise TypeError("Query must be a string")
        
        if parameters and not isinstance(parameters, Iterable):
            raise ValueError("Parameters must be interable: tuple, list or Row")

        # Prepare parameter
        
        # Execute query -> get result
        try:
            self.connection.call_query(sql, parameters)
        except Exception as e:
            raise ProgramingError(e)
        
        # Map column to description
        return True
        
    def executemany(self, sql: LiteralString, parameters: Iterable[str] = None) -> Self:
        pass
    
    def fetchone(self):
        pass
    
    def fetchmany(self, size: int):
        if not isinstance(size, int):
            raise TypeError("")
        
    
    def fetchall(self):
        pass
    
    def nextset(self):
        pass
    
    def setinputsizes(self, sizes):
        pass
    
    def setoutputsizes(self, sizes):
        pass
    
    def __iter__(self) -> Self:
        return self
    
    def __next__(self):
        try:
            self._current_row = next(self._data)
            return self._current_row
        except StopIteration:
            return StopIteration
    
    