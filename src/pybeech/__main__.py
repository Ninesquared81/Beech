"""Main script for pybeech package."""

from src.pybeech.lexer import Lexer
from src.pybeech.parser import Parser

source = """
hello {
    "world" !
}
General Kenobi  # You are a bold one
~{
    this is a
    block comment
}~
"""
lexer = Lexer(source)

print(*lexer, sep="\n")

parser = Parser(source)
print(parser.parse())
