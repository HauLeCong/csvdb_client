

__all__ = [
    "Warning",
    "Error",
    "InterfaceError",
    "DatabaseError",
    "DataError",
    "OperationalError",
    "IntegrityError",
    "InternalError",
    "ProgramingError",
    "NotSupportedError"
]

class Warning(Exception):
    """
    Exception raised for important warnings like data truncations while inserting, etc.
    """
    def __init__(self, *args):
        super().__init__(*args)
        
class Error(Exception):
    """
    Exception that is the base class of all other error exceptions. 
    You can use this to catch all errors with one single except statement. 
    """
    def __init__(self, *args):
        super().__init__(*args)
        
class InterfaceError(Error):
    """
    Exception raised for errors that are related to the database interface rather than the database itself.
    """
    def __init__(self, *args):
        super().__init__(*args)
        
class DatabaseError(Error):
    """
    Exception raised for errors that are related to the database.
    """
    def __init__(self, *args):
        super().__init__(*args)
        
class DataError(DatabaseError):
    """
    Exception raised for errors that are due to problems with the processed data like division by zero, numeric value out of range, etc.
    """
    def __init__(self, *args):
        super().__init__(*args)
        
class OperationalError(DatabaseError):
    """
    Exception raised for errors that are related to the database’s operation and not necessarily under the control of the programmer, e.g. an unexpected disconnect occurs, the data source name is not found, a transaction could not be processed, a memory allocation error occurred during processing, etc.
    """
    
    def __init__(self, *args):
        super().__init__(*args)
        
        
class IntegrityError(DatabaseError):
    """
    Exception raised when the relational integrity of the database is affected, e.g. a foreign key check fails.
    """
    def __init__(self, *args):
        super().__init__(*args)
        
class InternalError(DatabaseError):
    """
    Exception raised when the database encounters an internal error, e.g. the cursor is not valid anymore, the transaction is out of sync, etc.
    """
    def __init__(self, *args):
        super().__init__(*args)
        
class ProgramingError(DatabaseError):
    """
    Exception raised for programming errors, e.g. table not found or already exists, syntax error in the SQL statement, wrong number of parameters specified, etc.
    """ 
    def __init__(self, *args):
        super().__init__(*args)
        
class NotSupportedError(DatabaseError):
    """
    Exception raised in case a method or database API was used which is not supported by the database, e.g. requesting a .rollback() on a connection that does not support transaction or has transactions turned off.
    """
    def __init__(self, *args):
        super().__init__(*args)
        