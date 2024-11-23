
from typing import List
from enum import Enum
import re

from ..token import ReservedWord, Token
from ..ast_node import (
    AST, 
    SelectNode, 
    CreateTableNode,
    ColumnListNode,
    ColumnNode,
    ColumnNameNode,
    ColumnWildCardNode,
    ExprNode, 
    WhereNode,
    FromNode,
    ExprAddNode,
    ExprMultiNode,
    ExprValueNode,
    PredicateNode,
    ValueNode
)

class Parser:
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
        self.current_token = None
        self.iter_token = None
        self.current_character = next(self.iter_query_string)
        self.last_character = None
        self.character_count = 1
        self.token_index = 0
    
    def next_character(self):
        try:
            self.last_character = self.current_character
            self.current_character = next(self.iter_query_string)
        except StopIteration:
            raise
            
    def peek_next(self, whole_literal: str , regex_end_character) -> str:
        try:
            self.current_character = next(self.iter_query_string)
            if regex_end_character.search(self.current_character):
                return whole_literal
            else:
                return self.peek_next(whole_literal + self.current_character, regex_end_character)
        except StopIteration as e:
            raise ValueError("Literal not closed")
    
    def scan_number(self) -> str:
        """
            Scan number until meet end regex
        """
        def scan_util(s, end_reg):
            try:
                self.next_character()
                if end_reg.search(self.current_character):
                    return s
                return scan_util(s + self.current_character, end_reg) 
            except:
                return s
        scan_number = scan_util(self.current_character, re.compile(r"[ \t\r\n\,\*\/\+\-\.\<\>\=\(\)]"))
        if self.current_character == ".":
            # meet dot then scan again
            scan_number = scan_util(scan_number + self.current_character, re.compile(r"[ \t\r\n\,\*\/\+\-\.\<\>\=\(\)]"))
            return scan_number
        return scan_number
        
        
    def scan_string(self) -> None:
        """
            return a string identifier
            example: 
            _abc is valid
            "abc" is valid
        """
        def scan_until(s, end_reg):
            self.next_character()
            if end_reg.search(self.current_character):
                return s
            return scan_until(s + self.current_character, end_reg)
        
        if self.current_character == "\"":
            self.next_character()
            # The first character is the " then we only care about the endclose "
            # Keep scan until meet "
            try:  
                _whole_string = scan_until(self.current_character, re.compile(r"\""))
                # Consume " so that we can continue to next character
                self.next_character()
                return _whole_string
            except StopIteration:
                raise ValueError(f"Invalid token string was not closed")
            
        return scan_until(self.current_character, re.compile(r"[ \t\r\n\,\*\/\+\-\.\<\>\=\(\)]"))
         
    def scan(self):
        """
        Loop through each character and append to the token list a matched lexemes
        """
        keep_scan = True
        while keep_scan:
            try:
                match self.current_character:
                    case "(":
                        self.token.append((Token.LEFT_PAREN, ))
                    case ")":
                        self.token.append((Token.RIGHT_PAREN, ))
                    case ",":
                        self.token.append((Token.COMMA, ))
                    case "+":
                        self.token.append((Token.PLUS, ))
                    case "-":
                        self.token.append((Token.MINUS, ))
                    case "/":
                        self.token.append((Token.DIVIDE, ))
                    case ">":
                        self.next_character()
                        if self.current_character == "=":
                            self.token.append((Token.GREATER_THAN_EQUAL, ))
                        else:
                            self.token.append((Token.GREATER_THAN, ))
                            continue
                    case "<":
                        self.next_character()
                        if self.current_character == "=":
                            self.token.append((Token.LESS_THAN_EQUAL, ))
                        elif self.current_character == ">":
                            self.token.append((Token.DIFFERENT, ))
                        else:
                            self.token.append((Token.LESS_THAN, ))
                            continue
                    case "=":
                        self.token.append((Token.EQUAL, ))
                    case "*":
                        self.token.append((Token.ASTERISK, ))
                    case "'": # String literal
                        self.token.append((Token.STRING_LITERAL, self.peek_next("", re.compile(r"'"))))
                    case _: # Reversed word | Column name | Table name | Not support
                        # Number literal
                        if re.search(r"[0-9]", self.current_character):
                            whole_number = self.scan_number()
                            if not re.search(r"([0-9]+(\.[0-9]+)?|\.[0-9]+)$", whole_number):
                                raise ValueError(f"Invalid token [{whole_number}]")
                            try:
                                self.token.append((Token.NUMBER_LITERAL, float(whole_number)))
                            except Exception:
                                raise ValueError(f"Invalid token f{whole_number}")
                            continue
                        # Dot
                        elif self.current_character == ".":
                            # Check float number without digit exp: .123
                            if re.search(r"[ \,\+\-\*\/\=\<\>]", self.last_character):
                                whole_number = self.scan_number()
                                if not re.search(r"([0-9]+(\.[0-9]+)?|\.[0-9]+)$", whole_number):
                                    raise ValueError(f"Invalid token [{whole_number}]")
                                try:
                                    self.token.append((Token.NUMBER_LITERAL, float(whole_number)))
                                except Exception:
                                    raise ValueError(f"Invalid token [{whole_number}]")
                                continue
                            # Then this is an identifier
                            else:
                                self.token.append((Token.DOT, ))
                                pass
                                                            
                        # Identifier
                        elif re.search(r"[\w\"_]", self.current_character):
                            whole_word = self.scan_string()
                            if whole_word in [w.value for w in ReservedWord]:
                                self.token.append((ReservedWord[whole_word], ))
                                continue
                            else:
                                # Check again if they are valid regex for identifier 
                                if not re.search("^[^\d\W]\w*\Z", whole_word):
                                    raise ValueError(f"Invalid token [{whole_word}]")
                                self.token.append((Token.IDENTIFIER, whole_word))
                                continue   
                        # Ignore character space|\t|\r\n
                        elif re.search(r"[ \t\r\n]", self.current_character):
                            if re.search(r"[ \r\n]", self.current_character):
                                self.current_line += 1
                                self.current_position = 0
                            pass                            
                        else:
                            raise ValueError(f"Not support character {self.current_character} at line {self.current_line} position {self.current_position}")
                self.next_character()
            except StopIteration as e:
                keep_scan = False
    
    def advance_token(self) -> None:
        """
            To the next token
        """
        try:
            self.current_token = next(self.iter_token)
            self.token_index = self.token_index + 1
        except StopIteration:
            self.current_token = None
            pass
    
    def match_token(self, token) -> bool:
        """
        Check if current token match a Token|ReservedWord class
        """
        if self.current_token[0] == token:
            return True
        return False
    
    def parse(self) -> AST:
        """
        Create ast tree 
        """
        self.iter_token = iter(self.token)  
        self.advance_token()
        if self.match_token(ReservedWord.SELECT):
            self.advance_token()
            ast = AST(self.parse_select_clause())
        elif self.match_token(ReservedWord.CREATE):
            self.advance_token()
            if not self.match_token(ReservedWord.TABLE):
                raise ValueError(f"Expect token CREATE got {self.current_token}")
            ast = AST(self.parse_create_clause)
        else:
            raise ValueError(f"Invalid query expect SELECT or CREATE TABLE command got f{self.current_token}")
        return ast
 
    def parse_select_clause(self) -> SelectNode:
        """
        Parse token to SelectNode
        """
        # Check nothing so don't advance
        column_list = self.parse_column_list() 
        from_clause = None
        where_clause = None
        if self.match_token(ReservedWord.FROM):
            self.advance_token()
            from_clause = self.parse_from_clause()
            if self.match_token(ReservedWord.WHERE):
                self.advance_token()
                where_clause = self.parse_where_clause()
        return SelectNode(
                    column_list=column_list, 
                    from_clause=from_clause, 
                    where_clause=where_clause
                )
        
    def parse_from_clause(self) -> FromNode:
        if self.match_token(Token.IDENTIFIER):
            return FromNode(expr=self.current_token[1])
        return None
    
    def parse_where_clause(self) -> WhereNode:
        return WhereNode(expr=self.parse_predicate())
        
    def parse_column_list(self) -> ColumnListNode:
        """
        Parse token to columnlist node
        """
        # 
        current_left = ColumnListNode(left=self.parse_column(), right=None, operator=None)
        while self.match_token(Token.COMMA): 
            operator = self.current_token[0]
            self.advance_token()
            previous_left = current_left
            current_left = ColumnListNode(left=previous_left, right=self.parse_column(), operator=operator)
        return current_left   
        
    def parse_column(self) -> ColumnNode:
        """
        Parse token to ColumnNode
        """
        if self.match_token(Token.ASTERISK):
            column_node = ColumnNode(expr=self.parse_column_wild_card())
            return column_node
        else:
            star_index = self.token_index
            column_node = ColumnNode(expr = self.parse_expr())
            column_node.name = " ".join([str(value[1]) if len(value) > 1 else value[0].value for value in self.token[star_index-1:self.token_index]])
            
            if self.current_token and not self.match_token(ReservedWord.FROM):
                if self.match_token(Token.COMMA):
                    return column_node
                elif self.match_token(ReservedWord.AS) or self.match_token(Token.IDENTIFIER):
                    print(f"match AS {self.current_token}" )
                    self.advance_token()
                    column_node.alias = self.current_token
                    self.advance_token()
                    return column_node
                else:
                    raise ValueError(f"Unexpected token {self.current_token}")
            else:
                return column_node
    
    def parse_predicate(self) -> PredicateNode:
        from .predicate_parser import PredicateParser
        predicate_parser = PredicateParser(self)
        return predicate_parser.parse()
    
    def parse_expr(self) -> ExprNode:
        """
            Parse expression from token list
        """
        from .expression_parser import ExpressionParser
        expression_parser = ExpressionParser(self)
        return expression_parser.parse()
    
    def parse_column_wild_card(self) -> ColumnWildCardNode:
        column_wild_card =  ColumnWildCardNode()
        self.advance_token()
        return column_wild_card
                   
    def parse_create_clause(self) -> CreateTableNode:
        pass
    
