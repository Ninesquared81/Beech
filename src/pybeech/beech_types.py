"""Module containing all the runtime types of Beech."""
from __future__ import annotations

import typing


class Symbol:
    def __init__(self, value: str) -> None:
        self._value = value

    def __repr__(self) -> str:
        # Use value's own `repr` method to reduce assumptions.
        return f"{type(self).__name__}({repr(self._value)})"

    def __str__(self) -> str:
        # Wrap in an extra call to `str` in case a subclass changes the value type
        return str(self._value)

    def __hash__(self) -> int:
        return hash(self._value)

    def __getitem__(self, item) -> Symbol:
        return Symbol(self._value[item])


Key = typing.Union[str, Symbol]
Value = typing.Union[Key, 'Tree', 'List']
Tree = dict[Key, Value]
List = list[Value]
