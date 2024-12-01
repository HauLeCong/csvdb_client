from ..token import Token, ReservedWord
from ..ast_node import (
    ExprNode,
    ExprAddNode,
    ExprMultiNode,
    ExprValueNode,
    ExprParentNode,
    ValueNode,
)
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
        return ExprNode(expr=self._parse_expr_add())

    def _parse_expr_add(self) -> ExprAddNode:
        """
        Left recursive parse `ExprAddNode`
        Returns:
            `ExpreAddNode`
        """
        current_left = ExprAddNode(left=self._parse_expr_multi(), right=None, operator=None)
        while self._caller.current_token and (
            self._caller.match_token(Token.PLUS) or self._caller.match_token(Token.MINUS)
        ):
            current_operator = self._caller.current_token[0]
            self._caller.advance_token()
            previous_left = current_left
            current_left = ExprAddNode(
                left=previous_left,
                right=self._parse_expr_multi(),
                operator=current_operator,
            )
        return current_left

    def _parse_expr_multi(self) -> ExprMultiNode:
        """
        Left recursive parse `ExprMultiNode`
        Returns:
            `ExprMultiNode`
        """
        current_left = ExprMultiNode(left=self._parse_expr_value(), right=None, operator=None)
        while self._caller.current_token and (
            self._caller.match_token(Token.ASTERISK) or self._caller.match_token(Token.DIVIDE)
        ):
            current_operator = self._caller.current_token[0]
            previous_left = current_left
            self._caller.advance_token()
            current_left = ExprMultiNode(
                left=previous_left,
                right=self._parse_expr_value(),
                operator=current_operator,
            )
        return current_left

    def _parse_expr_value(self) -> ExprValueNode:
        """
        Parse `ExprValueNode`
        Returns:
            `ExprValueNode`
        """
        if (
            self._caller.current_token
            and self._caller.match_token(Token.NUMBER_LITERAL)
            or self._caller.match_token(Token.STRING_LITERAL)
        ):
            expr_value_node = ExprValueNode(expr=self._caller.current_token)
            self._caller.advance_token()
            return expr_value_node
        return ExprValueNode(expr=self._parse_value())

    def _parse_value(self) -> ValueNode:
        """
        Parse `ValueNode`
        Returns: `ValueNode`
        """
        if self._caller.current_token and self._caller.match_token(Token.IDENTIFIER):
            value_node = ValueNode(expr=self._caller.current_token)
            self._caller.advance_token()
            return value_node
        return ValueNode(expr=self._parse_expr_parent())

    def _parse_expr_parent(self) -> ExprParentNode:
        """
        Parse `ValueNode`
        Retunrs: `ValueNode`
        """
        if self._caller.match_token(Token.LEFT_PAREN):
            expr_value = self.parse()
            self._caller.advance_token()
            if self._caller.current_token and not self._caller.match_token(Token.RIGHT_PAREN):
                raise RuntimeError("( was not closed")
            return ExprParentNode(expr=expr_value)
        raise ValueError(f"Invalid token {self._caller.current_token}")
