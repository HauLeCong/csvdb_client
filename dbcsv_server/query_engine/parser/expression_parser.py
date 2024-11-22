from ..token import Token, ReservedWord
from ..ast_node import ExprNode, ExprAddNode, ExprMultiNode, ExprValueNode
from . import Parser

class ExpressionParser:
    
    """
        A parser to parse expression node        
        call parse() -> ExprNode    
    """
    
    def __init__(self, caller: Parser):
        self._caller = caller
        
    def parse(self, *args, **kwargs) -> ExprNode:
        """
        Parse `ExprNode`
        Returns:
            `ExprNode`
        """
        return ExprNode(expr=self.parse_expr_add_node())
    
    def _parse_expr_add_node(self) -> ExprAddNode:
        """
        Left recursive parse `ExprAddNode`
        Returns:
            ExpreAddNode
        """
        current_left = ExprAddNode(left = self._parse_expr_multi_node(), right=None, operator=None)
        while self._caller.current_character and (self._caller.match_token(Token.PLUS) or self._caller.match_token(Token.MINUS)):
            current_operator = self._caller.current_token[0]
            previous_left = current_left
            self._caller.advance_token()
            current_left = ExprAddNode(left = previous_left, right = self._parse_expr_multi_node(), operator=current_operator)
        return current_left
    
    def _parse_expr_multi_node(self) -> ExprMultiNode:
        """
        Left recursive parse `ExprMultiNode`
        Returns:
            `ExprMultiNode`
        """
        current_left = ExprMultiNode(left=self._parse_expr_value_node, right = None, operator= None)
        while self._caller.current_token and (self._caller.match_token(Token.ASTERISK) or self._caller.match_token(Token.DIVIDE)):
            current_operator = self._caller.current_token[0]
            previous_left = current_left
            self._caller.advance_token()
            current_left = ExprMultiNode(left= previous_left, right=self._parse_expr_value_node(), operator=current_operator)
            return current_left
    
    def _parse_expr_value_node(self) -> ExprValueNode:
        """
        Parse `ExprValueNode`
        Returns:
            `ExprValueNode`
        """
        pass