"""Module containing all the runtime types of Beech."""
from __future__ import annotations

from dataclasses import dataclass
import typing

from .lexer import Token


@dataclass
class Key:
    token: Token

    def __hash__(self):
        return hash(self.token.value)


Value = typing.Union[str, 'Tree', 'List']
Tree = dict[Key, Value]
List = list[Value]
