"""Provide an enum for the types of token accepted by the lexer and parser"""

import dataclasses
import enum


TokenTypes = enum.Enum("TokenTypes", [
    "L_PAREN",
    "R_PAREN",
    "L_SQBKT",
    "R_SQBKT",
    "L_BRACE",
    "R_BRACE",
    "INT_LIT",
    "FLOAT_LIT",
    "STR_LIT",
    "NAME",
    "COMMENT",
])


TOKEN_PATTERNS = {
    r"""\(""": "L_PAREN",
    r"""\)""": "R_PAREN",
    r"""\[""": "L_SQBKT",
    r"""]""": "R_SQBKT",
    r"""{""": "L_BRACE",
    r"""}""": "R_BRACE",
    r"""(?<![a-fA-F0-9.x])-?((0x[a-fA-F0-9]+)|([0-9]+))(?![a-fA-F0-9.x])""": "INT_LIT",
    r"""(?<![a-fA-F0-9.x])-?([0-9]+(\.[0-9]*)?|\.[0-9]+)(e[+-]?[0-9]+)?(?![a-fA-F0-9.x])""": "FLOAT_LIT",
    r""""([ !#-[\]-~]|\\[\\ntr0"'])*"|'([ -&(-[\]-~]|\\[\\ntr0"'])*'""": "STR_LIT",
    r"""([!$-&*,/:-z|]|~(?!#))([!$-&*-z|]|~(?!#))*|[+\-.]([!-&*-/:-z|~][!-&*-z|~]*)?""": "NAME",
    r"""(~#([ -"$-~](#(?!~))?)*#~)|(#[ -~]*)""": "COMMENT",
}


assert list(TOKEN_PATTERNS.values()) == list(TokenTypes._member_names_), "'TOKEN_PATTERNS' does not match 'TokenTypes'"


@dataclasses.dataclass
class Token:
    """A Beech syntax token, having a type and a value"""
    token_type: TokenTypes
    token_value: str
