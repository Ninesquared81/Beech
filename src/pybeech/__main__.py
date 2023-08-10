"""Main script for pybeech package."""
from typing import Union

from src.pybeech.beech_types import Symbol
from src.pybeech.default_mode.symbol_parser import parse_symbol
from src.pybeech.lexer import Lexer
from src.pybeech.parser import Parser
from src.pybeech.transformer import transformer

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
list (
    "this" is a
    list of ~{comment}~
    many, (items)
)
number 42
date 2023-08-10
"""
lexer = Lexer(source)

print(*lexer, sep="\n")

parser = Parser(source)
tree = parser.parse()
print(tree)


# class NumberSymbol(Symbol):
#     def __init__(self, number: int):
#         super().__init__(str(int))
#         self._number = number
#
#     def __repr__(self) -> str:
#         return f"NumberSymbol({self._number})"
#
#
# def transform_symbol(symbol: Symbol) -> Union[NumberSymbol, Symbol]:
#     try:
#         return NumberSymbol(int(str(symbol)))
#     except ValueError:
#         return symbol
#

trans = transformer(transform_symbol=parse_symbol)
print(trans(tree))
