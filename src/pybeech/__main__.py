"""Main script for pybeech package."""

from src.pybeech.lexer import Lexer
from src.pybeech.parser import Parser

source = r"""
hello {
    "world" !
}
General Kenobi  # You are a bold one
~{
    this is a
    block comment
}~
string "This is a
       'multiline "string", \
       "which includes escaped \
       'characters.
       "\t\x00 \x37 \u0041\b\f\a\v"
"""
lexer = Lexer(source)

print(*lexer, sep="\n")

parser = Parser(source)
print(parser.parse())
