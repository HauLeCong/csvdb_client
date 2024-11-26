from .exceptions import *
from .connection import Connection
from .cursor import Cursor

paramstyle = "pymark"  # -- WHERE name=%s
threadsafety = 1
apilevel = "2.0"

__version__ = 0.0


def connect(path_file: str) -> Connection:
    return Connection(path_file)
