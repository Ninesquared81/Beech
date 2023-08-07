"""Module containing all the runtime types of Beech."""
from __future__ import annotations

import typing


class Symbol:
    def __init__(self, value: str) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"Symbol('{self._value}')"

    def __str__(self) -> str:
        return self._value

    def __hash__(self) -> int:
        return hash(self._value)

Value = typing.Union[str, 'Tree', 'List']
Tree = dict[Key, Value]
List = list[Value]
