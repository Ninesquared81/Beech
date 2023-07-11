"""Parse Beech source code into a Beech Tree object."""

from .lexer import Lexer
from .types import Tree


class Parser:
    def __init__(self, source: str):
        self._lexer = Lexer(source)

    def parse(self) -> Tree:
        """Parse the source code."""

