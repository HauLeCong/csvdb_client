from collections.abc import Iterator, Iterable
from typing import LiteralString, Self


class Cursor(Iterator):
    def __init__(self) -> None:
        pass
    
    @property
    def description(self):
        pass
    
    def callproc(self):
        pass
    
    def close(self):
        pass
    
    def execute(self, sql: LiteralString, parameters: Iterable[str]) -> Self:
        pass
    
    def executemany(self, sql: LiteralString, parameters: Iterable[str]) -> Self:
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
    