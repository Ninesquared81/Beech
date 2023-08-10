"""Extension types defined for default mode."""

from dataclasses import dataclass


@dataclass
class Date:
    """ISO 8601 date."""

    year: int
    month: int
    day: int

    def __str__(self) -> str:
        return f"{self.year}-{self.month:02}-{self.day:02}"

    def __hash__(self) -> int:
        return hash(str(self))
