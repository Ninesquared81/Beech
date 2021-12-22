"""Provide an enum for the types of token accepted by the lexer and parser"""

import dataclasses

import enum


TokenTypes = enum.Enum("TokenTypes", [
    "DELIMITER",
    "INT_LIT",
    "FLOAT_LIT",
    "STR_LIT",
    "NAME",
    "COMMENT",
])


TOKEN_PATTERNS = {
    r"""[{(})]""": "DELIMITER",
    r"""-?((0x[a-fA-F0-9]+)|([0-9]+))""": "INT_LIT",
    r"""([0-9]+(\.[0-9]*)?|\.[0-9]+)(e[+-]?[0-9]+)?""": "FLOAT_LIT",
    r""""([ !#-[\]-~]|\\[\\ntr0"'])*"|'([ -&(-[\]-~]|\\[\\ntr0"'])*'""": "STR_LIT",
    r"""[!-&*,/:-z|~][!-&*-z|~]*|[+\-.]([!-&*-/:-z|~][!-&*-z|~]*)?""": "NAME",
    r"""(~#([ -"$-~](#(?!~))?)*#~)|(#[ -~]*)""": "COMMENT",
}


@dataclasses.dataclass
class Token:
    """A Beech syntax token, having a type and a value"""
    token_type: TokenTypes
    token_value: str
