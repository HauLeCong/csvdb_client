from enum import Enum    

class ReservedWord(Enum):
    SELECT = "SELECT"
    CREATE = "CREATE"
    FROM = "FROM"
    TABLE = "TABLE"
    WHERE = "WHERE"
    AS = "AS"

class Token(Enum):
    PLUS = "+"
    MINUS = "-"
    DIVIDE = "/"
    ASTERISK = "*"
    GREAT_THAN = ">"
    LESS_THAN = "<"
    GREATE_THAN_EQUAL = ">="
    LESS_THAN_EQUAL = "<="
    EQUAL = "="
    COMMA = ","
    DOUBLE_EQUAL = "=="
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    STRING_LITERAL = "STRING_LITERAL"
    NUMBER_LITERAL = "NUMBER_LITERAL"
    ALIAS_NAME = "ALIAS_NAME"
    INDENTIFIER = "INDENTIFIER"