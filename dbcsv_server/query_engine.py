
from dataclasses import dataclass
from typing import Literal, Optional, List, Union
from enum import Enum
import re

from .ast_node import AST, ArimethicNode, FactorNode, TermNode
    
class ReservedWord(Enum):
    SELECT = "SELECT"
    CREATE = "CREATE"
    FROM = "FROM"
    TABLE = "TABLE"
    WHERE = "WHERE"
    AS = "AS"

class Token(Enum):
    WILD_CARD_COL = "*"
    PLUS = "+"
    MINUS = "-"
    DIVIDE = "/"
    ASTERISK = "*"
    GREAT_THAN = ">"
    LESS_THAN = "<"
    GREATE_THAN_EQUAL = ">="
    LESS_THAN_EQUAL = "<="
    EQUAL = "="
    DOUBLE_EQUAL = "=="
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    STRING_LITERAL = "STRING_LITERAL"
    NUMBER_LITERAL = "NUMBER_LITERAL"
    ALIAS_NAME = "ALIAS_NAME"
    INDENTIFIER = "INDENTIFIER"


class QueryParser:
    """
        This class convert a sql string to an AST tree
    """
    def __init__(self, query_string: str):
        if not isinstance(query_string, str):
            raise ValueError("Only accept string argument")
        self.query_string = str.upper(query_string) + "\r\n"
        self.iter_query_string = iter(self.query_string)
        self.query_string_length = len(query_string)
        self.current_line = 1
        self.current_position = 0
        self.token = []
        self.current_character = next(self.iter_query_string)
        self.character_count = 1
    
    def peek_next(self, whole_literal: str , regex_end_character):
        print(whole_literal)
        try:
            self.current_character = next(self.iter_query_string)
            if regex_end_character.search(self.current_character):
                return whole_literal
            else:
                return self.peek_next(whole_literal + self.current_character, regex_end_character)
        except StopIteration as e:
            raise ValueError("Literal not closed")
         
    def scan(self):
        keep_scan = True
        while keep_scan:
            print(self.current_character)
            try:
                match self.current_character:
                    case "(":
                        self.token.append((Token.LEFT_PAREN, ))
                    case ")":
                        self.token.append((Token.RIGHT_PAREN, ))
                    case "+":
                        self.token.append((Token.PLUS, ))
                    case "-":
                        self.token.append((Token.MINUS, ))
                    case "/":
                        self.token.append((Token.DIVIDE, ))
                    case "=":
                        self.token.append((Token.EQUAL, ))
                    case "*":
                        self.token.append((Token.ASTERISK, ))
                    case "==":
                        self.token.append((Token.DOUBLE_EQUAL, ))
                    case "'": # String literal
                        self.token.append((Token.STRING_LITERAL, self.peek_next("", re.compile(r"'"))))
                    case "\"": # Identifier in double quote
                        self.token.append((Token.INDENTIFIER, self.peek_next("", re.compile(r"\""))))
                    case _: # Reversed word | Column name | Table name | Not support
                        # Number literal
                        if re.search(r"[0-9]", self.current_character):
                            literal_number = self.peek_next(self.current_character, re.compile(r"[^\d]"))
                            self.token.append((Token.NUMBER_LITERAL, literal_number))
                        # Identidier
                        elif re.search(r"[\w]", self.current_character):
                            whole_word = self.peek_next(self.current_character, re.compile(r"[ \t\r\n]"))
                            if whole_word in [w.value for w in ReservedWord]:
                                self.token.append((ReservedWord[whole_word], ))
                            else:
                                # Check again if they are valid regex for identifier 
                                if not re.search("^[^\d\W]\w*\Z", whole_word):
                                    raise ValueError(f"Invalid identifier {whole_word}")
                                self.token.append((Token.INDENTIFIER, whole_word))
                                
                        # Ignore character space|\t|\r\n
                        elif re.search(r"[ \t\r\n]", self.current_character):
                            if re.search(r"[ \r\n]", self.current_character):
                                self.current_line += 1
                                self.current_position = 0
                            pass                            
                        else:
                            raise ValueError(f"Not support character {self.current_character} at line {self.current_line} position {self.current_position}")
                self.current_character = next(self.iter_query_string)
            except StopIteration as e:
                keep_scan = False
        
    def parse_arimethic(self):
        pass
    
    def parse_term(self) -> TermNode:
        pass
    
    def parse_factor(self) -> FactorNode:
        # Initial 
        if re.search(r"[\d]", self.current_token):
            factor = FactorNode(self.current_token)
            self.current_token = self.next_token()
            return factor
        elif self.match_token("("):
            self.current_token = self.next_token()
            factor = FactorNode(self.parse_arimethic())
            self.expect(")")
            return factor
        else:
            raise RuntimeError(f"Expect number or (<expr>) got {self.current_token}")

class QueryPlanner:
    """
        This class convert a AST to plan of AST nodes
    """
    
    def __init__(self):
        pass
        
    def build(self, ast: AST) -> 'ExecutionPlan':
        pass
    
class ExecutionPlan:
    
    def __init__(self, nodes: List["ExecutionNode"]):
        pass
    

class ExecutionNode:
    pass