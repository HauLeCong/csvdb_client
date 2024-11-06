from dataclasses import dataclass
from typing import Literal, Optional, List, Union
from enum import Enum
import re

ComparisionOperator = Literal[">", "<", "=", "<>"]
AddtionOperator = Literal["+", "-"]
FactorOperator = Literal["*", "/"]

@dataclass
class AST:
    """
        <root> :: = <select_list> | <create_list>   
    """
    nodes: List[Union["SelectNode", "CreateTableNode"]]

@dataclass
class SelectNode:
    """
        `<select>` :: = SELECT `<column_list>` FROM `<from_clause>` WHERE `<where_clause>`
    """
    type = "Select"
    column_list: "ColumnListNode"
    from_clause: "FromNode"
    where_clause: "WhereNode"
    
       
@dataclass
class CreateTableNode:
    """
        <create_table> ::= CREATE TABLE <table_name> <table_element_list>
    """
    type = "Create"
    table_name: "IdentifierNode"
    table_element_list: "TableElementListNode"
    
@dataclass
class WhereNode:
    """
        <where_clause> ::= <logical> | <where_clause>
    """
    type = "Where"
    expr: "LogicalNode" | "WhereNode"
    
@dataclass
class FromNode:
    """
        <from_clause> ::= <identifier>
    """
    type =  "From"
    expr: "IdentifierNode"
    
@dataclass
class ColumnListNode:
    """
        `<column_list>` :: = <column>, <column_list> | <column>
    """
    type = "ColumnList"
    expr: "ColumnNode" | 'ColumnListNode'
    operator: Literal[","]

@dataclass
class ColumnNode:
    """
        `<column>` :: = `<column_wild_card>` [AS `<alias>::= <str>`] | `<expr>`
    """
    type =  "Column"
    expr: "ExprNode" | "ColumnWildCardNode"
    alias: Optional[str]
    
@dataclass
class ColumnWildCardNode:
    """
        <column_wild_card> ::= "*"
    """
    type = "ColumnWildCard"
    values = "*"

@dataclass
class TableElementListNode:
    """
        `<table_element_list>` ::= "(" `<table_element>`[{"," `<table_element>`}] ")"
    """
    type = "TableElementList"
    expr: "TableElementNode"
    
@dataclass
class TableElementNode:
    """
        `<table_element>` ::= `<identifier>`
    """
    type = "TableElement"
    expr: "IdentifierNode"
    
@dataclass
class ExprNode:
    type = "Expr"
    value: "IdentifierNode" | "LogicalNode" | "ComparisionNode" | "ArimethicNode"

@dataclass
class IdentifierNode:
    """
        `<indentifier>` :: = `<str>`
    """
    type = "Indentifier"
    value: str
    
@dataclass
class LogicalNode:
    """
        `<logical>` ::= `<logical_term>` | `<logical_node>` OR `<logical_term>`
    """
    left: "LogicalTermNode" | "LogicalNode"
    right: "LogicalTermNode"
    operator: Literal["OR"]
    
@dataclass
class LogicalTermNode:
    """
        `<logical_term>` ::= `<logical_factor>` | `<logical_term>` AND `<logical_factor>` 
    """
    left: "LogicalFactorNode" | "LogicalTermNode"
    right: "LogicalFactorNode"
    operator: Literal["AND"]

@dataclass
class LogicalFactorNode:
    """
        `<logical_factor>` ::= ["NOT"] `<literal_boolean>` 
    """
    expr: "LiteralBoolean"
    operator: Literal["NOT"] 

@dataclass
class ArimethicNode:
    """
        `<arimethic>` :: = `<term>`
        | `<arimethic>` "+" `<term>`
        | `<arimethic>` "-" `<term>`
    """
    type = "Arimethic"
    left: "TermNode" | "ArimethicNode"
    right: "TermNode"
    operator: AddtionOperator
    
@dataclass
class TermNode:
    """
        `<term>` :: = `<factor>`
        | `<term>` "*" `<factor>`
        | `<term> "/" <factor>`
    """
    type = "Term"
    left: "FactorNode" | "TermNode"
    right: "FactorNode"
    operator: FactorOperator

@dataclass
class FactorNode:
    """`<factor>` :: = ["+"]`<literal_number>` | ["-"]`<literal_number>` 
    """
    type = "Factor"
    expr: "LiteralNumber"
    operator: AddtionOperator
    

@dataclass
class ComparisionNode:
    pass
   
@dataclass
class LiteralNumber:
    """
        `<literal_number>`:: = int
    """
    type = "LiteralNumber"
    value: int
    
@dataclass
class LiteralString:
    """
        `<literal_string>` :: = str
    """
    type = "Literal String"
    value: str
    
@dataclass 
class LiteralBoolean:
    """
        `<literal_boolean>` :: = boolean
    """
    type = "Boolean"
    value: bool
    
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
    MULTIPLE = "*"
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
        self.query_string = str.upper(query_string) + "\r\n"
        self.iter_query_string = iter(self.query_string)
        self.query_string_length = len(query_string)
        self.current_line = 1
        self.current_position = 0
        self.token = []
        self.current_character = next(self.iter_query_string)
        self.character_count = 1
    
    def done_scan(self):
        return self.character_count == len(self.query_string)
    
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
                    case "'": # String literal
                        self.token.append((Token.STRING_LITERAL, self.peek_next("", re.compile(r"'"))))
                    case "\"": # Maybe alias
                        self.token.append((Token.ALIAS_NAME, self.peek_next("", re.compile(r"\""))))
                    case _: # Reversed word | Column name | Table name | Not support
                        # Number literal
                        if re.search(r"[0-9]", self.current_character):
                            self.token.append((Token.NUMBER_LITERAL, self.peek_next(self.current_character, re.compile(r"[^\d]"))))
                        # Identidier
                        elif re.search(r"[\w]", self.current_character):
                            whole_word = self.peek_next(self.current_character, re.compile(r"[ \t\r\n]"))
                            if whole_word in [w.value for w in ReservedWord]:
                                self.token.append((ReservedWord[whole_word], ))
                            else:
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
        
    def parse(self):
        pass

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