"""Extension types defined for default mode."""
from __future__ import annotations

from dataclasses import dataclass


class StrHashMixin:
    """Mixin for a class whose hash is just that of its string value."""
    def __hash__(self) -> int:
        return hash(str(self))


@dataclass
class Date(StrHashMixin):
    """ISO 8601 date."""

    year: int
    month: int
    day: int

    def __str__(self) -> str:
        return f"{self.year:04}-{self.month:02}-{self.day:02}"


@dataclass
class Time(StrHashMixin):
    """ISO 8601 time."""

    hour: int
    minute: int
    second: int
    tz_hour: int | None = None
    tz_minute: int | None = None  # Note: this is only used if `tz_hour` is not None.

    def __str__(self) -> str:
        simple_time = f"{self.hour:02}:{self.minute:02}:{self.second:02}"
        tz_offset = (f"{self.tz_hour:+03}{f':{self.tz_minute:02}' if self.tz_minute is not None else ''}"
                     if self.tz_hour is not None else "")
        return f"{simple_time}{tz_offset}"


@dataclass
class DateTime(StrHashMixin):
    """ISO 8601 date and time."""

    date: Date
    time: Time

    def __str__(self) -> str:
        return f"{self.date}T{self.time}"
