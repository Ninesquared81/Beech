"""Parse Beech source code into a Beech Tree object."""

from .lexer import Lexer


class Parser:
    def __int__(self, source: str):
        self._lexer = Lexer(source)

    def parse(self):
        """Parse the source code."""

