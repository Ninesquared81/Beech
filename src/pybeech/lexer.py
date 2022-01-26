"""Provide a class for lexing Beech tokens"""

import re

from src.pybeech.errors import BeechSyntaxError
from src.pybeech.beech_token import Token, TokenTypes, TOKEN_PATTERNS


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


def _file_mode(filename: str):
    with open(filename) as file:
        source_code = file.read()
    lexer = Lexer(source_code)
    print(*lexer.tokenize(), sep="\n")


def _interactive_mode():
    print("Interactive mode\nEnter '!q' or '!quit' to quit")
    while True:
        line = input().rstrip()
        if line.lower() in ("!q", "!quit"):
            break
        try:
            print(*Lexer(line).tokenize(), sep="\n")
        except BeechSyntaxError as e:
            print(e)


def main():
    from sys import argv

    if len(argv) == 1:
        _interactive_mode()
    else:
        _file_mode(argv[1])


if __name__ == "__main__":
    main()
