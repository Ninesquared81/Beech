"""Perform lexical analysis on Beech files."""

from __future__ import annotations

from dataclasses import dataclass
import enum

from .errors import LexError


class TokenType(enum.Enum):
    """Enum for a token's type."""
    LEFT_BRACE = "'{' token"
    RIGHT_BRACE = "'}' token"
    LEFT_BRACKET = "'(' token"
    RIGHT_BRACKET = "')' token"
    STRING = "string token"
    SYMBOL = "symbol token"
    COMMENT = "comment token"
    WHITESPACE = "whitespace token"

    EMPTY = "empty token"

    def __bool__(self) -> bool:
        return self != type(self).EMPTY


@dataclass
class Token:
    """A Beech syntax token."""
    type: TokenType
    start_index: int
    value: str


class Lexer:
    """A class to lex Beech source files on the fly."""
    def __init__(self, source: str) -> None:
        self._source: str = source
        self._index: int = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._is_at_end():
            raise StopIteration
        return self.next_token()


    def next_token(self) -> Token:
        """Get the next valid token in source."""
        token_type: TokenType = TokenType.EMPTY
        start: int = self._index
        value: str = ""

        # An empty token is returned if already at the end of tokens.

        if self._peek().isspace():
            token_type = TokenType.WHITESPACE
            self._consume_whitespace()
        elif self._match('"') or self._match("'"):
            token_type = TokenType.STRING
            value = self._string()
        elif self._match("#"):
            token_type = TokenType.COMMENT
            self._comment_line()
        elif self._match("~{"):
            token_type = TokenType.COMMENT
            self._comment_block()
        elif self._match("}~"):
            raise LexError("Unmatched '}~'")
        elif self._is_symbolic():
            token_type = TokenType.SYMBOL
            self._symbol()
        elif self._match("{"):
            token_type = TokenType.LEFT_BRACE
        elif self._match("}"):
            token_type = TokenType.RIGHT_BRACE
        elif self._match("("):
            token_type = TokenType.LEFT_BRACKET
        elif self._match(")"):
            token_type = TokenType.RIGHT_BRACKET
        elif not self._is_at_end():
            raise LexError(f"Invalid character {self._peek()}")

        return Token(type=token_type, start_index=start, value=value or self._source[start:self._index])

    def next_non_space(self) -> Token:
        """Get the next non-whitespace token in source."""
        self._consume_whitespace()
        return self.next_token()

    def _advance(self, n: int = 1) -> None:
        # Don't check for end of source. This is checked by the lexer anyway
        self._index += n

    def _is_at_end(self) -> bool:
        return self._index >= len(self._source)

    def _check(self, seq: str):
        # Note: slice will be empty if already at the end.
        return seq == self._source[self._index:self._index + len(seq)]

    def _consume_whitespace(self) -> None:
        while self._peek().isspace():
            self._advance()

    def _is_reserved(self) -> bool:
        return self._check("~{") or self._peek() in "'\"{}()#"

    def _is_symbolic(self) -> bool:
        if self._is_at_end():
            return False
        c = self._peek()
        return c.isprintable() and not c.isspace() and not self._is_reserved()

    def _match(self, seq: str) -> bool:
        if not self._check(seq):
            return False
        self._advance(len(seq))
        return True

    def _peek(self) -> str:
        # Use a slice to return "" if already at end.
        return self._source[self._index:self._index + 1]

    def _previous(self) -> str:
        assert self._index > 0, "No previous character."
        return self._source[self._index - 1]

    def _string(self) -> str:
        opener: str = self._previous()
        out_string: str = ""
        start_index: int = self._index
        while not self._is_at_end():
            if self._match("\\"):
                out_string += self._source[start_index:self._index - 1]
                start_index = self._index + 1  # Index of character after escape sequence
                if self._check("\n"):
                    continue  # Handle the multiline string separately.
                if self._match("'") or self._match('"') or self._match("\\"):
                    start_index -= 1  # Index of escaped character
                elif self._match("n"):
                    out_string += "\n"
                elif self._match("r"):
                    out_string += "\r"
                elif self._match("t"):
                    out_string += "\t"
                elif self._match("f"):
                    out_string += "\f"
                elif self._match("\b"):
                    out_string += "\b"
                else:
                    raise LexError("Invalid escape sequence.")
            elif self._match(opener):
                out_string += self._source[start_index:self._index - 1]
                return out_string  # End of string.
            elif self._match("\n"):
                # Multiline string.
                out_string += self._source[start_index:self._index]
                self._consume_whitespace()
                if not self._is_at_end() and (self._match("'") or self._match('"')):
                    opener = self._previous()
                    start_index = self._index
                else:
                    raise LexError("Unterminated string literal.")
            elif self._peek().isprintable():
                self._advance()
            else:
                raise LexError(f"Illegal character in string literal: {hex(ord(self._peek()))}")

        raise LexError("Unterminated string literal.")

    def _comment_block(self) -> None:
        while not self._match("}~"):
            if self._match("~{"):
                self._comment_block()
            self._advance()

    def _comment_line(self) -> None:
        while not self._is_at_end() and not self._check("\n"):
            self._advance()

    def _symbol(self) -> None:
        while self._is_symbolic():
            self._advance()
