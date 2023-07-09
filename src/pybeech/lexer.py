"""Perform lexical analysis on Beech files."""

from __future__ import annotations

from dataclasses import dataclass
import enum


class TokenType(enum.Enum):
    """Enum for a token's type."""
    LEFT_BRACE = "'{' token"
    RIGHT_BRACE = "'}' token"
    LEFT_BRACKET = "'(' token"
    RIGHT_BRACKET = "')' token"
    STRING = "string token"
    SYMBOL = "symbol token"

    EMPTY = "empty token"

    def __bool__(self) -> bool:
        return self != type(self).EMPTY


@dataclass(kw_only=True)
class Token:
    """A Beech syntax token."""
    type: TokenType
    start_index: int
    length: int
    rest: str

    def value(self) -> str:
        end = self.start_index + self.length
        return self.rest[self.start_index:end]


class Lexer:
    """A class to lex Beech source files on the fly."""
    def __init__(self, source: str) -> None:
        self._source: str = source
        self._index: int = 0

    def next_token(self) -> Token:
        """Get the next valid token in the source file."""
        token_type: TokenType = TokenType.EMPTY
        start: int = self._index

        return Token(type=token_type, start_index=start, length=self._index - start, rest=self._source[start:])

    def _advance(self) -> None:
        self._index += 1
        if self._is_at_end():
            raise EOFError("Unexpected EOF when scanning token.")

    def _is_at_end(self) -> bool:
        return self._index >= len(self._source)

    def _match(self, c: str) -> bool:
        if self._is_at_end() or self._peek() != c:
            return False
        self._advance()
        return True

    def _peek(self) -> str:
        try:
            return self._source[self._index]
        except IndexError:
            raise EOFError("Unexpected EOF when scanning token.")
