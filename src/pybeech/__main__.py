"""Main script for pybeech package."""

from src.pybeech.lexer import Lexer

source = "{'hello' 0}"
lexer = Lexer(source)

print(*(f"{token.type = }, {token.value() = }\n" for token in lexer))
