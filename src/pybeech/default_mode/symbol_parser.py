"""Module containing the default symbol transformations."""
from __future__ import annotations

import re

from src.pybeech.beech_types import Symbol
from .extension_types import Date


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

    def __init__(self, year: int, month: int, day: int):
        super().__init__("")
        self._value = Date(year, month, day)

    @classmethod
    def try_parse(cls, value: str) -> DateSymbol | None:
        """Try to parse the value as an ISO 8601 date, or return None if failed."""
        date_match = re.match(
            r"^(?P<year>[0-9]{4})-(?P<month>0[1-9]|1[0-2])-(?P<day>0[1-9]|[12][0-9]|3[01])$",
            value)
        if date_match is None:
            return None
        return cls(**{k: int(v) for k, v in date_match.groupdict().items()})


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
