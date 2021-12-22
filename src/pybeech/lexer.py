"""Provide a class for lexing Beech tokens"""

import enum
import re

from .token import Token, TokenTypes, TOKEN_PATTERNS
from .errors import BeechSyntaxError


class Lexer:
    """Perform lexical analysis on Beech source code"""

    def __init__(self, source_code: str):
        self.code = source_code

    def _scan(self, curr_token_pos: int) -> tuple[Token, int]:
        """Scan current token and return its value and the position of the next token."""
        rest = self.code[curr_token_pos:]
        rest_trimmed = rest.lstrip()
        n_spaces_removed = len(rest) - len(rest_trimmed)

        for pattern, token_type in TOKEN_PATTERNS.items():
            if (m := re.match(pattern, rest_trimmed)):
                token_value = m.group()
                next_token_pos = curr_token_pos + n_spaces_removed + len(token_value)
                return Token(TokenTypes[token_type], token_value), next_token_pos

        # no match => the token was invalid
        raise BeechSyntaxError(f"Invalid token: {rest_trimmed}")

    def tokenize(self) -> list[Token]:
        """Return the list of tokens in the source code"""
        token_pointer = 0
        tokens: list[Token] = []
        while token_pointer < len(self.code):
            token, token_pointer = self._scan(token_pointer)
            tokens.append(token)
        return tokens
