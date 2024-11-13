
from typing import List
from enum import Enum
import re

from .token import ReservedWord, Token
from .ast_node import (
    AST, 
    SelectNode, 
    CreateTableNode,
    ColumnListNode,
    ColumnNode,
    ColumnNameNode,
    ColumnWildCardNode,
    ArimethicNode,
    ComparisionNode,
    LogicalNode,
    TermNode,
    FactorNode,
    ExprNode
)

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
        self.current_token = None
        self.iter_token = None
        self.current_character = next(self.iter_query_string)
        self.character_count = 1
    
    def peek_next(self, whole_literal: str , regex_end_character) -> str:
        try:
            self.current_character = next(self.iter_query_string)
            if regex_end_character.search(self.current_character):
                return whole_literal
            else:
                return self.peek_next(whole_literal + self.current_character, regex_end_character)
        except StopIteration as e:
            raise ValueError("Literal not closed")
    
    def scan_number(self, whole_number) -> str:
        """
            Scan number until meet end regex
        """
        try:
            self.current_character = next(self.iter_query_string) 
            # Match space | tab | endline then end scan
            if re.search(r"[^0-9.]", self.current_character):
                return whole_number
            return self.scan_number(whole_number+self.current_character)
        except:
            raise 
        
    def scan_string(self) -> None:
        """
            return a string identifier
            example: 
            _abc is valid
            "abc" is valid
        """
        def scan_util(s, end_reg):
            self.current_character = next(self.iter_query_string)
            if end_reg.search(self.current_character):
                return s
            return scan_util(s + self.current_character, end_reg)
        
        _whole_string = ""
        if self.current_character == "\"":
            self.current_character = next(self.iter_query_string)
            # The first character is the " then we only care about the endclose "
            # Keep scan until meet "
            try:  
                _whole_string = scan_util(self.current_character, re.compile(r"\""))
                return _whole_string
            except StopIteration:
                raise ValueError(f"Invalid token string was not closed")
        return scan_util(_whole_string + self.current_character, re.compile(r"[ \t\r\n\,]"))
         
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
                    case "=":
                        self.token.append((Token.EQUAL, ))
                    case "*":
                        self.token.append((Token.ASTERISK, ))
                    case "==":
                        self.token.append((Token.DOUBLE_EQUAL, ))
                    case "'": # String literal
                        self.token.append((Token.STRING_LITERAL, self.peek_next("", re.compile(r"'"))))
                    case _: # Reversed word | Column name | Table name | Not support
                        # Number literal
                        if re.search(r"[0-9.]", self.current_character):
                            whole_number = self.scan_number(self.current_character)
                            if not re.search(r"([0-9]+(\.[0-9]+)?|\.[0-9]+)$", whole_number):
                                raise ValueError(f"Invalid token {whole_number}")
                            self.token.append((Token.NUMBER_LITERAL, float(whole_number)))
                            continue
                        # Identifier
                        elif re.search(r"[\w\"_]", self.current_character):
                            whole_word = self.scan_string()
                            if whole_word in [w.value for w in ReservedWord]:
                                self.token.append((ReservedWord[whole_word], ))
                            else:
                                # Check again if they are valid regex for identifier 
                                if not re.search("^[^\d\W]\w*\Z", whole_word):
                                    raise ValueError(f"Invalid token {whole_word}")
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
    
    def advance_token(self) -> None:
        """
            To the next token
        """
        try:
            self.current_token = next(self.iter_token)
        except StopIteration:
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
        from_clause = self.parse_from_clause()
        where_clause = self.parse_where_clause()
        return SelectNode(column_list=column_list, from_clause=from_clause, where_clause=where_clause)
        
    def parse_column_list(self) -> ColumnListNode:
        """
        Parse token to columnlist node
        """
        # 
        self.parse_column()
    
    def parse_column(self) -> ColumnNode:
        """
        Parse token to ColumnNode
        """
        self.advance_token()
        if self.match_token(Token.ASTERISK):
            column_node = ColumnNode(expr=self.parse_column_wild_card)
        elif self.match_token(Token.INDENTIFIER):
            column_node = ColumnNode(expr=self.parse_column_name())
            if self.match_token(Token.ALIAS_NAME):
                column_node.alias = self.current_token
        else:
            column_node = ColumnNode(expr = self.parse_expr())

    def parse_expr(self) -> ExprNode:
        """
            Parse expression from token list
            This is LL(0) so we try to parse one by one until all fail or one success by order
        """
        # Try arimethic first then logical then comparision 
        for _parse in [self.parse_arimethic, self.parse_logical, self.parse_commparision]:
            try:
                result = _parse()
                return ExprNode(expr=result)
            except:
                pass
        # If all fail
        raise RuntimeError(f"Unable to parse f{self.current_token}")
    
    def parse_arimethic(self) -> ArimethicNode:
        current_left = ArimethicNode(left = self.parse_term(), right = None, operator= None)
        while self.match_token(Token.PLUS) or self.match_token(Token.MINUS):
            operator = self.current_token[0]
            self.advance_token()
            previous_left = current_left
            current_left = ArimethicNode(left = previous_left, right=self.parse_term(), operator=operator)
        return current_left
    
    def parse_logical(self) -> LogicalNode:
        pass
    
    def parse_commparision(self) -> ComparisionNode:
        pass
    
    def parse_term(self) -> TermNode:
        # Initial
        current_left = TermNode(left=self.parse_factor(), right= None, operator=None)
        while self.match_token(Token.ASTERISK) or self.match_token(Token.DIVIDE):
            operator = self.current_token[0]
            self.advance_token()
            previous_left = current_left
            current_left = TermNode(left=previous_left, right=self.parse_factor(), operator=operator)
        return current_left 
    
    def parse_factor(self) -> FactorNode:
        # Initial 
        if self.match_token(Token.LEFT_PAREN):
            self.advance_token()  # Move to the next token
            factor = FactorNode(self.parse_arimethic())
            if not self.match_token(Token.RIGHT_PAREN):
                raise ValueError(f"Expected token )")
        else:
            if not isinstance(self.current_token[1], (int, float, bool)):
                raise ValueError(f"Expect (expr) or int|float|bool value got {self.current_token}")
            factor = FactorNode(expr = self.current_token[1])
            self.advance_token()
        return factor
    
    def parse_column_name(self) -> ColumnNameNode:
        pass
    
    def parse_column_wild_card(self) -> ColumnWildCardNode:
        pass
     
    def parse_from_clause(self):
        pass
    
    def parse_where_clause(self):
        pass
    
    def parse_create_clause(self) -> CreateTableNode:
        pass
    
