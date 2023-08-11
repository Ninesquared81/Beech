"""Module containing the default symbol transformations."""
from __future__ import annotations

import re

from src.pybeech.beech_types import Symbol
from .extension_types import Date, Time, DateTime


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

    @property
    def value(self):
        return self._value


class TimeSymbol(Symbol):
    """Symbol representing a time in the ISO 8601 format."""

    def __init__(self, hour: int, minute: int, second: int, tz_hour: int | None = None, tz_minute: int | None = None) -> None:
        super().__init__("")
        self._value = Time(hour, minute, second, tz_hour, tz_minute)

    @classmethod
    def try_parse(cls, value: str) -> TimeSymbol | None:
        """Try to parse the value as an ISO 8601 time, or return None if failed."""
        time_match = re.match(
            r"^T?(?P<hour>[01][0-9]|2[0-4]):(?P<minute>[0-5][0-9]):(?P<second>[0-5][0-9]|60)"
            r"(?P<timezone>Z|[-+\u2212](?:[01][0-9]|2[0-4]):?[0-5][0-9])?$",
            value
        )
        if time_match is None:
            return None
        time_dict = time_match.groupdict()
        timezone = time_dict.pop("timezone")
        if timezone is not None:
            hour, minute = "0", "0"
            if timezone != "Z":
                # tz_offset = timezone.replace("\u2212", "-").replace(":", "")
                hour, minute = re.match(r"([+-]?\d{2}):?(\d{2})", timezone).groups()
            time_dict["tz_hour"] = hour
            time_dict["tz_minute"] = minute
        return cls(**{k: int(v) for k, v in time_dict.items()})

    @property
    def value(self):
        return self._value


class DateTimeSymbol(Symbol):
    """Symbol representing a date and time in the ISO 8601 format."""

    def __init__(self, date: Date, time: Time):
        super().__init__("")
        self._value = DateTime(date, time)

    @classmethod
    def try_parse(cls, value: str):
        date_part, t, time_part = value.partition("T")
        if t == "":
            return None
        if (date := DateSymbol.try_parse(date_part)) is None:
            return None
        if (time := TimeSymbol.try_parse(t + time_part)) is None:
            return None
        return cls(date.value, time.value)


EXTENDED_SYMBOLS = [
    NumberSymbol,
    DateSymbol,
    TimeSymbol,
    DateTimeSymbol,
]


def parse_symbol(symbol: Symbol) -> Symbol:
    """Parse a symbol into its corresponding default mode subtype."""
    value = str(symbol)
    for cls in EXTENDED_SYMBOLS:
        if (sym := cls.try_parse(value)) is not None:
            return sym
    return TextSymbol(value)
