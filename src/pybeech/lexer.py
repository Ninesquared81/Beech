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
        """Get the next valid token in the source file."""
        self._consume_whitespace()

        token_type: TokenType = TokenType.EMPTY
        start: int = self._index
        value: str = ""

        if self._match('"') or self._match("'"):
            token_type = TokenType.STRING
            value = self._string()
        elif self._match("#"):
            token_type = TokenType.COMMENT
            self._comment()
        elif self._peek().isalnum():
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
        else:
            raise LexError(f"Invalid character {self._peek()}")

        return Token(type=token_type, start_index=start, value=value or self._source[start:self._index])

    def _advance(self) -> None:
        if self._is_at_end():
            raise LexError("Unexpected EOF when scanning token.")
        self._index += 1

    def _is_at_end(self) -> bool:
        return self._index >= len(self._source)

    def _check(self, c: str):
        if not self._is_at_end() and self._peek() == c:
            return True
        return False

    def _consume_whitespace(self) -> None:
        while not self._is_at_end():
            # Match any whitespace characters
            if self._match(" "):
                continue
            if self._match("\t"):
                continue
            if self._match("\n"):
                continue
            return  # No more whitespaces found

    def _is_reserved(self) -> bool:
        return self._peek() in set("'\"{}()")

    def _match(self, c: str) -> bool:
        if not self._check(c):
            return False
        self._advance()
        return True

    def _peek(self) -> str:
        try:
            return self._source[self._index]
        except IndexError:
            raise LexError("Unexpected EOF when scanning token.")

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

    def _comment(self) -> None:
        if self._match("{"):
            self._comment_block()
        else:
            self._comment_line()

    def _comment_block(self) -> None:
        while not (self._match("}") and self._match("#")):
            if self._match("#") and self._match("{"):
                self._comment_block()

    def _comment_line(self) -> None:
        while not self._is_at_end() and not self._check("\n"):
            self._advance()

    def _symbol(self) -> None:
        while not self._peek().isspace() and not self._is_reserved():
            if not self._peek().isprintable():
                raise LexError(f"Illegal character in symbol.")
            self._advance()
