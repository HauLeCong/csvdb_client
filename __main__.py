# from .dbapi2 import co

import sqlite3
import inspect

class A:
    def __init__(self):
        self.status = "open"
        
class B:
    def __init__(self, conn: A):
        self.connection = conn
        
a = A()
b = B(a)

print(b.connection.status)

a.status = "closed"
print(b.connection.status)