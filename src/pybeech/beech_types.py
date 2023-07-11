"""Module containing all the runtime types of Beech."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Union

from .lexer import Token


@dataclass
class Key:
    token: Token

    def __hash__(self):
        return hash(self.token.value)


class Tree:
    def __init__(self) -> None:
        self._comments: list[Token] = []
        self._data: dict[Key, Value] = {}

    def add_comment(self, comment: Token) -> None:
        self._comments.append(comment)

    def insert_kv_pair(self, key: Key, value: Value) -> None:
        self._data[key] = value

    @property
    def data(self) -> dict[Key, Value]:
        return self._data.copy()

    @property
    def comments(self) -> list[Token]:
        return self._comments[:]

    def __repr__(self) -> str:
        return f"<Tree: comments={self.comments}, data={self.data}>"


class List:
    def __init__(self) -> None:
        self._comments: list[Token] = []
        self._data: list[Value] = []

    def add_comment(self, comment: Token):
        self._comments.append(comment)

    def add_value(self, value: Value):
        self._data.append(value)

    @property
    def data(self) -> list[Value]:
        return self._data[:]

    @property
    def comments(self) -> list[Token]:
        return self._comments[:]


Value = Union[str, Tree, List]
