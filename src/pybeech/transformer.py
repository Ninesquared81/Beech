"""Module for transforming a general Beech AST into a specified one."""
from __future__ import annotations

from typing import Callable, TypeVar

from .beech_types import Symbol, Key, Value

T = TypeVar("T")
U = TypeVar("U")
Transform = Callable[[T], T]


def transformer(transform_symbol: Transform[Symbol] | None = None,
                transform_string: Transform[str] | None = None) -> Transform[Value]:
    """Return a transformation function for Beech values based on transformation rules for keys.

    :param transform_symbol: rule for transforming symbols into other symbols
    :param transform_string: rule for transforming strings into other strings

    :return: inferred transformation rule for any Beech value
    """
    def _identity(_x: T) -> T: return _x
    if transform_symbol is None:
        transform_symbol = _identity
    if transform_string is None:
        transform_string = _identity

    def transform_key(key: Key) -> Key:
        if isinstance(key, Symbol):
            return transform_symbol(key)
        if isinstance(key, str):
            return transform_string(key)
        raise TypeError(f"Unexpected key type: {type(key)}")

    def transform_value(value: Value) -> Value:
        if isinstance(value, Symbol):
            return transform_symbol(value)
        if isinstance(value, str):
            return transform_string(value)
        if isinstance(value, dict):
            return {transform_key(k): transform_value(v) for k, v in value.items()}
        if isinstance(value, list):
            return [transform_value(v) for v in value]
        raise TypeError(f"Unexpected value type: {type(value)}")

    return transform_value
