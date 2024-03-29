"""Module containing all exceptions raised by the package."""


class LexError(Exception):
    """Exception raised when a syntactical error occurs."""


class ParseError(Exception):
    """Exception raised in parsing."""
