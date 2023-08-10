"""Module containing the default symbol transformations."""
from __future__ import annotations

from src.pybeech.beech_types import Symbol


class TextSymbol(Symbol):
    """Symbol which is purely textual."""

    @classmethod
    def from_base_symbol(cls, symbol: Symbol) -> TextSymbol:
        return cls(str(symbol))


class NumberSymbol(Symbol):
    """Symbol representing a number."""

    def __init__(self, value: int) -> None:
        super().__init__("")  # Dummy value
        self._value = value

    @classmethod
    def try_parse(cls, value: str) -> NumberSymbol | None:
        """Try to parse the value as a number, or return None if failed."""
        try:
            return cls(int(value, base=0))
        except ValueError:
            return None


class DateSymbol(Symbol):
    """Symbol representing a date in the ISO 8601 format."""

    @classmethod
    def try_parse(cls, value: str) -> DateSymbol | None:
        """Try to parse the value as an ISO 8601 date, or return None if failed."""


EXTENDED_SYMBOLS = [
    NumberSymbol,
    DateSymbol,
]


def parse_symbol(symbol: Symbol) -> Symbol:
    """Parse a symbol into its corresponding default mode subtype."""
    value = str(symbol)
    for cls in EXTENDED_SYMBOLS:
        if (sym := cls.try_parse(value)) is not None:
            return sym
    return TextSymbol(value)
