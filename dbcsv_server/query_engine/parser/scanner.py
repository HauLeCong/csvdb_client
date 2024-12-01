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
                        self._add_token(Token.LEFT_PAREN)

                    case ")":
                        self._add_token(Token.RIGHT_PAREN)

                    case ",":
                        self._add_token(Token.COMMA)

                    case "+":
                        self._add_token(Token.PLUS)

                    case "-":
                        self._add_token(Token.MINUS)

                    case "/":
                        self._add_token(Token.DIVIDE)

                    case "=":
                        self._add_token(Token.EQUAL)

                    case "*":
                        self._add_token(Token.ASTERISK)

                    case ">":
                        next_char = self._next_character()
                        match next_char:
                            case "=":
                                self._add_token(Token.GREATER_THAN_EQUAL)
                            case _:
                                self._add_token(Token.GREATER_THAN)
                                continue

                    case "<":
                        next_char = self._next_character()
                        match next_char:
                            case "=":
                                self._add_token(Token.LESS_THAN_EQUAL)
                            case _:
                                self._add_token(Token.LESS_THAN_EQUAL)
                                continue

                    case "'":
                        self._add_token(
                            Token.STRING_LITERAL,
                            self._scan_util("", re.compile(r"['\]")),
                        )
                        if self._current_character != "'":
                            raise ValueError(
                                f"Quote not closed {self._current_position} at {self._current_line}"
                            )
                        continue

                    case '"':
                        self._add_token(Token.IDENTIFIER, self._scan_util("", re.compile(r"[\"]")))
                        if self._current_character != '"':
                            raise ValueError(
                                f"Double qoute not closed {self._current_position} at {self._current_line}"
                            )
                        continue

                    case ".":
                        if self._last_character and re.search(
                            r"[ \,\+\-\*\/\=\<\>]", self._last_character
                        ):
                            whole_number = self._scan_literal_number()
                            if not re.search(r"([0-9]+(\.[0-9]+)?|\.[0-9]+)$", whole_number):
                                raise ValueError(f"Invalid token [{whole_number}]")
                            try:
                                self._add_token(Token.NUMBER_LITERAL, float(whole_number))
                            except Exception:
                                raise ValueError(f"Invalid token [{whole_number}]")
                            continue

                    case _:
                        if re.search(r"[0-9]", self._current_character):
                            whole_number = self._scan_literal_number()
                            if not re.search(r"([0-9]+(\.[0-9]+)?|\.[0-9]+)$", whole_number):
                                raise ValueError(f"Invalid token [{whole_number}]")
                            try:
                                self._add_token(Token.NUMBER_LITERAL, float(whole_number))
                            except Exception:
                                raise ValueError(f"Invalid token f{whole_number}")
                            continue

                        elif re.search(r"[\w_]", self._current_character):
                            whole_ident = self._scan_util(
                                self._current_character,
                                re.compile(r"[ \t\r\n\,\*\/\+\-\.\<\>\=\(\)]"),
                            )
                            if whole_ident in [w.value for w in ReservedWord]:
                                self._add_token(ReservedWord[whole_ident])
                            else:
                                if not re.search("^[^\d\W]\w*\Z", whole_ident):
                                    raise ValueError(f"Invalid token [{whole_ident}]")
                                self._add_token(Token.IDENTIFIER, whole_ident)
                            continue

                        elif re.search(r"[ \t\r\n]", self._current_character):
                            if re.search(r"[\r\n]", self._current_character):
                                self._current_line += 1
                                self._current_position = 0
                            pass

                        else:
                            raise ValueError(
                                f"Unsupport character at {self._current_position} line {self._current_line}"
                            )

                self._next_character()
                self._current_position += 1
            except StopIteration:
                self._keep_scan = False
        return self._token

    def _scan_util(self, whole, end_reg) -> str:
        try:
            self._next_character()
            if end_reg.search(self._current_character):
                return whole
            return self._scan_util(whole + self._current_character, end_reg)
        except:
            return whole

    def _scan_literal_number(self) -> str:
        end_reg = re.compile(r"[ \t\r\n\,\*\/\+\-\.\<\>\=\(\)]")
        whole_number = self._scan_util(self._current_character, end_reg)
        if self._current_character == ".":

            whole_number = self._scan_util(whole_number + self._current_character, end_reg)
            print("**** scan again", whole_number)
            return whole_number
        return whole_number

    def _add_token(self, token, val=None) -> None:
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
