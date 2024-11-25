from ..token import Token, ReservedWord
from ..ast_node import (
    CreateTableNode, 
    TableNameNode, 
    TableDefinitionGroupNode, 
    TableDefinitionListNode, 
    TableDefinitionNode, 
    ColumnDefinitionNode,
    DatabaseNode
)
from . import Parser

class CreateTableParser:
    
    def __init__(self, caller: Parser):
        self._caller = caller
        
    def parse(self) -> CreateTableNode:
        if self._caller.match_token(Token.IDENTIFIER):
            database = DatabaseNode(expr=self._caller.current_token)
            self._caller.advance_token()
            if self._caller.match_token(Token.DOT):
                self._caller.advance_token()
                if self._caller.match_token(Token.IDENTIFIER):
                    table_name = TableNameNode(expr = self._caller.current_token)
                    self._caller.advance_token()
                    table_definition_group = self._parse_table_definition_group()
                    return CreateTableNode(database= database, table_name=table_name, table_definition_group=table_definition_group)
                raise ValueError(f"Expect table name got {self._caller.current_token}")
            raise ValueError(f"Unexpect token {self._caller.current_token}")
        raise ValueError(f"Expect database name got {self._caller.current_token}")
    
    def _parse_table_definition_group(self) -> TableDefinitionNode:
        if self._caller.match_token(Token.LEFT_PAREN):
            self._caller.advance_token()
            table_definition_group = TableDefinitionGroupNode(self._parse_table_definition_list())
            if self._caller.match_token(Token.RIGHT_PAREN):
                return table_definition_group
            raise ValueError(f"Expect close ) got {self._caller.current_token}")
        raise ValueError(f"Expect table definition list")
    
    def _parse_table_definition_list(self) -> TableDefinitionListNode:
        current_left = TableDefinitionListNode(left=self._parse_table_definition(), right=None)
        while self._caller.match_token(Token.COMMA):
            previous_left = current_left
            self._caller.advance_token()
            current_left = TableDefinitionListNode(left=previous_left, right=self._parse_table_definition())
        return current_left
    
    def _parse_table_definition(self) -> TableDefinitionNode:
        if self._caller.match_token(Token.IDENTIFIER):
            column_name = self._caller.current_token
            self._caller.advance_token()
            column_definition = self._parse_column_definition()
            return TableDefinitionNode(column_name=column_name, column_definition=column_definition)
        raise ValueError(f"Expect identifier got {self._caller.current_token}")
    
    def _parse_column_definition(self) -> ColumnDefinitionNode:
        if self._caller.match_token(ReservedWord.INT) or self._caller.match_token(ReservedWord.FLOAT) or self._caller.match_token(ReservedWord.STRING):
            column_definition = ColumnDefinitionNode(type_name=self._caller.current_token)
            self._caller.advance_token()
            return column_definition
        raise ValueError(f"Expect column type got {self._caller.current_token}")