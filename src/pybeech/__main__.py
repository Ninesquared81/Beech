"""Main script for pybeech package."""

from src.pybeech.lexer import Lexer

source = "{'hello' 0 \"there\\nhi\n'where\\\"'  # This is a line comment\n"\
         "~{This is a ~{nested}~ block comment}~} ~not-a-comment symbol~{comment}~"
lexer = Lexer(source)

print(*lexer, sep="\n")
