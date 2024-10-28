from .cursor import Cursor
from typing import Optional, Any
from .exceptions import ProgramingError, DatabaseError
from pathlib import PurePath
import requests


class Connection:
    def __init__(
        self,
        path_file: str,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
    ) -> None:
        if isinstance(path_file, str) or isinstance(path_file, PurePath):
            self.path_file = path_file
        else:
            raise TypeError("Invalid path_file, must be either string or Path")
        self.path_file = path_file
        self.user = user
        self.password = password
        self.host = host
        self._closed = 0
        self._row_count = -1

    @property
    def closed(self):
        return self._closed

    @property
    def rowcount(self):
        return self._rowcount

    @rowcount.setter
    def rowcount(self, number):
        self._row_count

    def close(self) -> None:
        """
        Close the connection now (rather than whenever .__del__() is called).
        The connection will be unusable from this point forward; an Error (or subclass) exception will be raised if any operation is attempted with the connection. The same applies to all cursor objects trying to use the connection. Note that closing a connection without committing the changes first will cause an implicit rollback to be performed.
        """
        self._closed = 1

    def commit(self):
        """
        Commit any pending transaction to the database.
        Note that if the database supports an auto-commit feature,
        this must be initially off. An interface method may be provided to turn it back on.
        Database modules that do not support transactions should implement this method with void functionality.
        """
        pass

    def rollback(self):
        """
        This method is optional since not all databases provide transaction support. [3]
        In case a database does provide transactions this method causes the database to roll back to the start of any pending transaction. Closing a connection without committing the changes first will cause an implicit rollback to be performed.
        """
        pass

    def cursor(self) -> Cursor:
        """
        Return a new Cursor Object using the connection.
        Raises:
            ProgramingError: On closed connection
        Returns:
            Cursor
        """
        if self._closed == 1:
            raise ProgramingError("Cannot operate on closed connection.")
        cursor = Cursor(self)
        return cursor

    def _execute_sql(self, query: str) -> None:
        """
        Call execute query from server

        Args:
            query (str): a sql query string

        Raises:
            ProgramingError: on closed connection

        Returns: json reponse
        """
        if self._closed == 1:
            raise ProgramingError("Cannot operate on closed connection.")
        response = requests.post(
            self.host, data={"path_file": self.path_file, "query": query}
        )

        if response.status_code != 200:
            raise DatabaseError("Server error, cannot process request.")
        return response.json()

    def _execute_no_sql(self, query: str) -> None:
        if self._closed == 1:
            raise ProgramingError("Cannot operate on closed connection.")
        response = requests.get(self.host, data={"query": query}).json()
        if response.status_code != 200:
            raise DatabaseError("Server error cannot process request.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_instance, traceback):
        self.close()
        return False
