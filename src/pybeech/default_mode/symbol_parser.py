"""Module containing the default symbol transformations."""
import enum

from src.pybeech.beech_types import Symbol


class SymbolType(enum.Enum):
    NUMBER = "number"
    DATE = "date-iso8601"
    TEXT = "text"


class TextSymbol(Symbol):
    """Symbol which is purely textual."""

    @classmethod
    def from_base_symbol(cls, symbol: Symbol) -> 'TextSymbol':
        return cls(str(symbol))


class NumberSymbol(Symbol):
    """Symbol representing a number."""

    def __init__(self, value: int) -> None:
        super().__init__("")  # Dummy value
        self._value = value


class DateSymbol(Symbol):
    """Symbol representing a date in the ISO 8601 format."""


class Parser:
    """Parse a symbol into its corresponding default mode subtype."""

    def __init__(self, symbol: Symbol) -> None:
        self._symbol = symbol
        self._options: set[SymbolType] = {t for t in SymbolType}
        self._index = 0

    def parse(self) -> Symbol:
        assert len(self._options) > 0
        while len(self._options) > 1:
            pass
        assert self._options == {SymbolType.TEXT}
        return TextSymbol(str(self._symbol))
