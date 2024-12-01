from .exceptions import ProgramingError


class Encoder:
    """
    Escape value of passing variable from client
    This copy from -mysql dbapi
    https://github.com/PyMySQL/PyMySQL/blob/main/pymysql/converters.py
    """

    def __init__(self):
        self._escape_table = [chr(x) for x in range(128)]
        self._escape_table[0] = "\\0"
        self._escape_table[ord("\\")] = "\\\\"
        self._escape_table[ord("\n")] = "\\n"
        self._escape_table[ord("\r")] = "\\r"
        self._escape_table[ord("\032")] = "\\Z"
        self._escape_table[ord('"')] = '\\"'
        self._escape_table[ord("'")] = "\\'"
        self.encoders = {
            int: self._escape_int,
            str: self._escape_string,
            type(None): self._escape_none,
            float: self._escape_float,
        }

    def escape_item(self, val):
        encoder = self.encoders.get(type(val))
        esc_val = encoder(val)
        return esc_val

    def _escape_string(self, str_val: str):
        return str_val.translate(self._escape_table)

    def _escape_int(self, int_val):
        return str(int_val)

    def _escape_none(self, none_val):
        return "NULL"

    def _escape_float(self, float_val):
        s = repr(float_val)
        if s in ("inf", "-inf", "nan"):
            raise ProgramingError("%s can not be used" % s)
        if "e" not in s:
            s += "e0"
        return s
