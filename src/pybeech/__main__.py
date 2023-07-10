"""Main script for pybeech package."""

from src.pybeech.lexer import Lexer

source = "{'hello' 0 \"there\\nhi\n'where\\\"'}"
lexer = Lexer(source)

print(*(token for token in lexer), sep="\n")
