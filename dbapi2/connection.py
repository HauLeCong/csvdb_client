from .cursor import Cursor
from typing import Optional 
from .exceptions import Error, Warning, InterfaceError, ProgramingError
from pathlib import PurePath

class Connection():
    def __init__(self, path_file: str, user: Optional[str]=None, password: Optional[str]=None, host: Optional[str]=None) -> None:
        if isinstance(path_file, str) or isinstance(path_file, PurePath):
            self.path_file = path_file
        else:
            raise TypeError("Invalid path_file, must be either string or Path")
        self.path_file = path_file
        self.user = user
        self.password = password
        self.host = host
        self._closed = 0

    @property
    def closed(self):
        return self._closed
    
    def close(self) -> None:
        self._closed = 1
    
    def commit(self):
        pass
    
    def rollback(self):
        pass
    
    def cursor(self) -> Cursor: 
        if self.closed == 1:
            raise ProgramingError("Cannot operate on closed connection")
        return Cursor()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exec_type, exec_msg, traceback):
        self.close()
