from ..token import Token, ReservedWord
from typing import List
import re


class Scanner:
    """
    A token scanner class
    Call scan() -> return a list of token
    :query_string: A sql query string
    """

    def __init__(self, query_string):
        self._keep_scan = True
        self._current_character = None
        self._iter_query_string = iter(query_string)
        self._query_string = str.upper(query_string + "\r\n")
        self._current_line = 0
        self._current_position = 0
        self._current_character = None
        self._last_character = None
        self._character_count = 0
        self._run_scan = False
        self._token = []

    def scan(self) -> List:
        self._next_character()
        self._keep_scan = True
        while self._keep_scan:
            try:
                match self._current_character:
                    case "(":
                        self._add_token(Token.LEFT_PAREN, None)

                    case ")":
                        self._add_token(Token.RIGHT_PAREN, None)

                    case ",":
                        self._add_token(Token.COMMA, None)

                    case "+":
                        self._add_token(Token.PLUS, None)

                    case "-":
                        self._add_token(Token.MINUS, None)

                    case "/":
                        self._add_token(Token.DIVIDE, None)

                    case "=":
                        self._add_token(Token.EQUAL, None)

                    case "*":
                        self._add_token(Token.ASTERISK, None)

                    case ">":
                        next_char = self._next_character()
                        match next_char:
                            case "=":
                                self._add_token(Token.GREATER_THAN_EQUAL, None)
                            case _:
                                self._add_token(Token.GREATER_THAN)
                                continue

                    case "<":
                        next_char = self._next_character()
                        match next_char:
                            case "=":
                                self._add_token(Token.LESS_THAN_EQUAL, None)
                            case _:
                                self._add_token(Token.LESS_THAN_EQUAL, None)
                                continue

                    case "'":
                        self._add_token(
                            Token.STRING_LITERAL,
                            self._scan_util("", re.compile("['\]")),
                        )
                        if self._current_character != "'":
                            raise ValueError("Quote not closed")
                        continue

                    case _:
                        if re.search(r"[0-9]", self._current_character):
                            whole_number = self.scan_number()
                            if not re.search(
                                r"([0-9]+(\.[0-9]+)?|\.[0-9]+)$", whole_number
                            ):
                                raise ValueError(f"Invalid token [{whole_number}]")
                            try:
                                self.token.append(
                                    (Token.NUMBER_LITERAL, float(whole_number))
                                )
                            except Exception:
                                raise ValueError(f"Invalid token f{whole_number}")
                            continue

            except StopIteration:
                self._keep_scan = False

    def _scan_util(self, whole, end_reg):
        try:
            self._next_character()
            if end_reg.search(self._current_character):
                return whole
            return self._scan_util(whole + self._current_character, end_reg)
        except StopIteration:
            return whole

    def _scan_literal_number(self):
        end_reg = re.compile(r"[ \t\r\n\,\*\/\+\-\.\<\>\=\(\)]")
        whole_number = self._scan_util(self._current_character, end_reg)
        if self._current_character == ".":
            whole_number = self._scan_util(
                whole_number + self._current_character, end_reg
            )
            return whole_number
        return whole_number

    def _scan_string_indentifier(self):
        pass

    def _add_token(self, token, val=None):
        if not isinstance(token, (Token, ReservedWord)):
            raise ValueError("Cannot append non token value")
        self._token.append((token, val))

    def _next_character(self) -> str:
        try:
            self._last_character = self._current_character
            self._current_character = next(self._iter_query_string)
            return self._current_character
        except StopIteration:
            self._run_scan = False
            raise

    def _scan_util(self, whole, reg_end):
        try:
            self._next_character()
            if reg_end.search(reg_end):
                return whole
            return self._scan_util(whole + self.current_character, reg_end)
        except:
            return whole

    def _():
        pass
