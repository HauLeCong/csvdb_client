from collections.abc import Iterator, Iterable
from typing import LiteralString, Self, List, Tuple
from .exceptions import *


class Cursor(Iterator):
    """
    These objects represent a database cursor, which is used to manage the context of a fetch operation.
    Cursors created from the same connection are not isolated, i.e., any changes done to the database by a cursor are immediately visible by the other cursors.
    Cursors created from different connections can or can not be isolated, depending on how the transaction support is implemented (see also the connection’s .rollback() and .commit() methods).

    Args:
        Iterator (_type_): _description_
    """

    def __init__(self, connection, data=None, description=None) -> None:
        self.connection = connection
        self.arraysize = 1
        self.description = description
        self._data = data
        self._current_row = None
        self._row_count = 0
        self._closed = 0
        self._current_index = 0

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: Iterable):
        self._data = data

    @property
    def description(self):
        """
        This read-only attribute is a sequence of 7-item sequences.
        Each of these sequences contains information describing one result column:
        - name
        - type_code
        - display_size
        - internal_size
        - precision
        - scale
        - null_ok

        This attribute will be None for operations that do not return rows or if the cursor has not had an operation invoked via the .execute*() method yet.
        The type_code can be interpreted by comparing it to the Type Objects specified in the section below.
        """
        return self._description

    @description.setter
    def description(self, metadata: tuple):
        self._description = metadata

    @property
    def arraysize(self):
        """
        This read/write attribute specifies the number of rows to fetch at a time with .fetchmany(). It defaults to 1 meaning to fetch a single row at a time.
        Implementations must observe this value with respect to the .fetchmany() method, but are free to interact with the database a single row at a time. It may also be used in the implementation of .executemany().
        """
        return self._arraysize

    @arraysize.setter
    def arraysize(self, size: int):
        if not isinstance(size, int):
            raise TypeError("Arraysize must be an integer")
        self._arraysize = size

    def callproc(self, proc: str, params: Iterable):
        """
        Call a stored database procedure with the given name. The sequence of parameters must contain one entry for each argument that the procedure expects. The result of the call is returned as modified copy of the input sequence.
        Input parameters are left untouched, output and input/output parameters replaced with possibly new values.
        The procedure may also provide a result set as output. This must then be made available through the standard .fetch*() methods.

        Args:
            proc (str): _description_
            params (Iterable): _description_
        """
        pass

    def close(self):
        """
        Close the cursor now (rather than whenever __del__ is called).
        The cursor will be unusable from this point forward; an Error (or subclass) exception will be raised if any operation is attempted with the cursor.
        """
        self._closed = 1

    def _prepare_query_param(self, sql: str, params: Iterable) -> str:
        pass

    def execute(self, sql: LiteralString, parameters: Iterable = None) -> Self:
        if self._closed == 1:
            raise ProgramingError("Cannot operate on a closed cursor.")

        if not isinstance(sql, str):
            raise TypeError("Query must be a string")

        if parameters and not isinstance(parameters, Iterable):
            raise ValueError("Parameters must be interable: tuple, list or Row")

        # Prepare parameter
        sql_str = self._prepare_query_param(sql, parameters)
        # Execute query -> get result
        try:
            response = self.connection._execute_sql(sql_str)
            self._data = response["data"]
            self._current_row = None
            self._current_index = 0
            self._row_count = len(response["data"])
            self._description = response["description"]
        except Exception as e:
            raise e

        return Cursor(self.connection, self._data, self._description)

    def executemany(
        self, sqls: List[LiteralString], parameters: Iterable[str] = None
    ):
        """
        Prepare a database operation (query or command) and then execute it against all parameter sequences or mappings found in the sequence seq_of_parameters.
        Modules are free to implement this method using multiple calls to the .execute() method or by using array operations to have the database process the sequence as a whole in one call.

        Use of this method for an operation which produces one or more result sets constitutes undefined behavior, and the implementation is permitted (but not required) to raise an exception when it detects that a result set has been created by an invocation of the operation.

        The same comments as for .execute() also apply accordingly to this method.

        Return values are not defined.

        Args:
            sqls (List[LiteralString]): _description_
            parameters (Iterable[str], optional): _description_. Defaults to None.
        """
        pass

    def fetchone(self):
        """
        Fetch the next row of a query result set, returning a single sequence, or None when no more data is available. [6]

        Raises:
            An Error (or subclass) exception is raised if the previous call to .execute*() did not produce any result set or no call was issued yet.
            OperationalError: Data not exists

        Returns:
            A data row
        """
        if not self._data and self._description:
            raise OperationalError("Data not exists")
        return self.__next__()

    def fetchmany(self, size: int = None):
        """
        Fetch the next set of rows of a query result, returning a sequence of sequences (e.g. a list of tuples). An empty sequence is returned when no more rows are available.
        The number of rows to fetch per call is specified by the parameter.
        If it is not given, the cursor’s arraysize determines the number of rows to be fetched. The method should try to fetch as many rows as indicated by the size parameter. If this is not possible due to the specified number of rows not being available, fewer rows may be returned.

        An Error (or subclass) exception is raised if the previous call to .execute*() did not produce any result set or no call was issued yet.

        Note there are performance considerations involved with the size parameter. For optimal performance, it is usually best to use the .arraysize attribute. If the size parameter is used, then it is best for it to retain the same value from one .fetchmany() call to the next.

        Args:
            size (int): [cursor.arraysize]

        Raises:
            TypeError: size musts be integer
            OperationalError: data not exists

        Returns:
            _type_: _description_
        """
        if size and not isinstance(size, int):
            raise TypeError("Size must be integer")
        if not self._data or not self._description:
            raise OperationalError("Data not exists")
        i = 0
        fetch_rows = size if size else self.arraysize
        fetched_data = []
        print(self.arraysize)
        while i < fetch_rows:
            try:
                fetched_data.append(self.__next__())
                i += 1
            except StopIteration as e:
                break
        print(fetched_data)
        return fetched_data

    def fetchall(self):
        """
        Fetch all (remaining) rows of a query result, returning them as a sequence of sequences (e.g. a list of tuples). Note that the cursor’s arraysize attribute can affect the performance of this operation.
        An Error (or subclass) exception is raised if the previous call to .execute*() did not produce any result set or no call was issued yet.

        Raises:
            OperationalError: data not exists

        Returns:
            _type_: _description_
        """
        if not self._data or not self._description:
            raise OperationalError("Data not exists")
        fetched_data = []
        while True:
            try:
                fetched_data.append(self.__next__())
            except StopIteration:
                break
        return fetched_data

    def nextset(self):
        pass

    def setinputsizes(self, sizes):
        """
        This can be used before a call to .execute*() to predefine memory areas for the operation’s parameters.
        sizes is specified as a sequence — one item for each input parameter. The item should be a Type Object that corresponds to the input that will be used, or it should be an integer specifying the maximum length of a string parameter.
        If the item is None, then no predefined memory area will be reserved for that column (this is useful to avoid predefined areas for large inputs).

        Args:
            sizes (_type_): _description_
        """
        pass

    def setoutputsizes(self, sizes):
        """
        Set a column buffer size for fetches of large columns (e.g. LONGs, BLOBs, etc.). The column is specified as an index into the result sequence. Not specifying the column will set the default size for all large columns in the cursor.
        This method would be used before the .execute*() method is invoked.

        Args:
            sizes (_type_): _description_
        """
        pass

    def __enter__(self):
        return self

    def __exit__(self, exec_msg, exec_type, traceback):
        self.close()
        return False

    def __iter__(self) -> Self:
        return self

    def __next__(self):
        if self._current_index < len(self.data):
            self._current_row = self._data[self._current_index]
            self._current_index += 1
            return self._current_row
        else:
            self._current_row = None
            raise StopIteration
