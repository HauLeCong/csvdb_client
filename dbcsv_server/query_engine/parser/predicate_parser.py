from ..ast_node import (
    PredicateNode,
    PredicateOrNode,
    PredicateAndNode,
    PredicateNotNode,
    PredicateCompareNode,
    PredicateParentNode,
)
from . import Parser
from ..token import Token, ReservedWord


class PredicateParser:
    """
    A parser to parse predicate node
    This class will visit Query Parser class to get require information
    """

    def __init__(self, caller: Parser):
        self._caller = caller

    def parse(self, *args, **kwargs) -> PredicateNode:
        return PredicateNode(expr=self._parse_predicate_or_node())

    def _parse_predicate_or_node(self) -> PredicateOrNode:
        """
        Parse `PredicateOrNode` (left recursive)
        Returns:
            `PredicateOrNode`
        """
        current_left = PredicateOrNode(
            left=self._parse_predicate_and_node(), right=None, operator=None
        )
        while self._caller.current_token and self._caller.match_token(
            ReservedWord.OR
        ):
            previous_left = current_left
            operator = self._caller.current_token[0]
            self._caller.advance_token()
            current_left = PredicateOrNode(
                left=previous_left,
                right=self._parse_predicate_and_node(),
                operator=operator,
            )
        return current_left

    def _parse_predicate_and_node(self) -> PredicateAndNode:
        """
        Parse `PredicateAndNode` (left recursive)
        Returns:
            `PredicateAndNode`
        """
        current_left = PredicateAndNode(
            left=self._parse_predicate_not_node(), right=None, operator=None
        )
        while self._caller.current_token and self._caller.match_token(
            ReservedWord.AND
        ):
            previous_left = current_left

            operator = self._caller.current_token[0]
            self._caller.advance_token()
            current_left = PredicateAndNode(
                left=previous_left,
                right=self._parse_predicate_not_node(),
                operator=operator,
            )
        return current_left

    def _parse_predicate_not_node(self) -> PredicateNotNode:
        """
        Parse `PredicateNotNode` 
        Returns:
            `PredicateNotNode`
        """
        if self._caller.match_token(ReservedWord.NOT):
            operator = self._caller.current_token[0]
            self._caller.advance_token()
            return PredicateNotNode(
                expr=self._parse_predicate_compare_node(), operator=operator
            )
        return PredicateNotNode(
            expr=self._parse_predicate_compare_node(), operator=None
        )

    def _parse_predicate_compare_node(self) -> PredicateCompareNode:
        """
        Parse `PredicateCompareNode`
        Returns: `PredicateCompareNode`
        """
        if self._caller.match_token(Token.LEFT_PAREN):
            self._caller.advance_token()
            predicate_parent = PredicateCompareNode(
                left=self._parse_predicate_parent(), right=None, operator=None
            )
            if not self._caller.match_token(Token.RIGHT_PAREN):
                raise ValueError(
                    f"Expected close ) got {self._caller.current_token}"
                )
            return predicate_parent
        else:
            current_left = PredicateCompareNode(
                left=self._caller.parse_expr(), right=None, operator=None
            )
            while self._caller.current_token and (
                self._caller.match_token(Token.EQUAL)
                or self._caller.match_token(Token.GREATER_THAN)
                or self._caller.match_token(Token.LESS_THAN)
                or self._caller.match_token(Token.GREATER_THAN_EQUAL)
                or self._caller.match_token(Token.LESS_THAN_EQUAL)
                or self._caller.match_token(Token.DIFFERENT)
            ):
                current_operator = self._caller.current_token[0]
                self._caller.advance_token()
                previous_left = current_left
                current_left = PredicateCompareNode(
                    left=previous_left,
                    right=self._caller.parse_expr(),
                    operator=current_operator,
                )
            return current_left

    def _parse_predicate_parent(self) -> PredicateParentNode:
        """
        Parse `PredicateParentNode`
        Returns: `PredicateParentNode`
        """
        predicate_parent_node = PredicateParentNode(expr=self.parse())
        return predicate_parent_node
