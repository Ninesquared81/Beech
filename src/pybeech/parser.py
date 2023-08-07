"""Parse Beech source code into a Beech Tree object."""
from __future__ import annotations

from .errors import ParseError
from .lexer import Lexer, Token, TokenType
from .beech_types import Tree, Key, Value, List


class Parser:
    def __init__(self, source: str):
        self._lexer = Lexer(source)
        self._current_token: Token = self._lexer.next_token()  # Start with the first token.
        self._previous_token: Token = Token.empty()  # Initialise with an empty token to avoid using None.
        self._current_tree: Tree | List = Tree()

    def parse(self) -> Tree:
        """Parse the source code."""
        return self._beech()

    def _beech(self) -> Tree:
        while not self._check(TokenType.EMPTY):
            self._consume_whitespace()
            if self._match(TokenType.SYMBOL) or self._match(TokenType.STRING):
                key = Key(self._previous_token)
                self._consume_whitespace(strict=True)
                value = self._value()
                if key in self._current_tree:
                    raise ParseError("Keys in a tree must be unique.")
                self._current_tree[key] = value
            else:
                break  # End of tree.
        return self._current_tree

    def _tree(self) -> Tree:
        previous_tree = self._current_tree
        new_tree: Tree = {}
        self._current_tree = new_tree
        self._beech()
        self._current_tree = previous_tree
        self._consume_whitespace()
        self._expect(TokenType.RIGHT_BRACE)
        return new_tree

    def _list(self) -> List:
        new_list: List = []
        previous_tree = self._current_tree
        self._current_tree = new_list
        while not self._check(TokenType.RIGHT_BRACKET) and not self._check(TokenType.EMPTY):
            new_list.append(self._value())
            if not self._check(TokenType.RIGHT_BRACKET):
                self._consume_whitespace(strict=True)
        self._expect(TokenType.RIGHT_BRACKET)
        self._current_tree = previous_tree
        return new_list

    def _value(self) -> Value:
        if self._match(TokenType.STRING):
            return self._previous_token.value
        elif self._match(TokenType.SYMBOL):
            return self._previous_token.value
        elif self._match(TokenType.LEFT_BRACE):
            return self._tree()
        elif self._match(TokenType.LEFT_BRACKET):
            return self._list()
        else:
            raise ParseError(f"Unexpected token {self._current_token}")

    def _advance(self):
        self._previous_token = self._current_token
        self._current_token = self._lexer.next_token()

    def _consume_whitespace(self, strict=False) -> None:
        if not self._match(TokenType.WHITESPACE) and strict:
            raise ParseError(f"Expect {TokenType.WHITESPACE}")

    def _expect(self, token_type: TokenType) -> None:
        if not self._match(token_type):
            raise ParseError(f"Expected {token_type} but got {self._current_token.type}")

    def _check(self, token_type: TokenType) -> bool:
        return self._current_token.type == token_type

    def _match(self, token_type: TokenType) -> bool:
        if not self._check(token_type):
            return False

        self._advance()
        return True
