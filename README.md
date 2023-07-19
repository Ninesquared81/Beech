# Beech
A simple tree-based language.

## Syntax
The syntax of Beech is based primarily around the tree data type. Beech also has string literals and symbols.

### Tree Literals
An _unordered_ tree is delimited by braces and has zero or more key-value pairs, with each key unique.
The key and value are separated by whitespace, as are the key-value pairs themselves:
`{` _key1_ &nbsp;_value1_ &nbsp;_key2_ &nbsp;_value2_ &nbsp;&hellip; `}`.

An _ordered_ tree is delimited by square brackets. Structure is implied by the order it is written in,
so keys may be duplicated:
`[` _key_ &nbsp;_value1_ &nbsp;_key_ &nbsp;_value2_ &nbsp;&hellip; `]`.

A third type of tree is a _list_, which is delimited by parentheses. This is syntactic sugar for an
unordered tree where the keys are 1, &hellip;, n for n items:
`(` _value1_ &nbsp;_value2_&nbsp;&nbsp;&hellip; `)`.

### String Literals
A string literal starts and ends with double or single quote marks. It can span multiple lines, with each
line starting with a fresh quote mark (either kind) and only the last line needing an ending quote mark,
which must match the mark which opened that line. There may be arbitrary whitespace before the continuing
quote mark. Any newline in a string is included in it, unless escaped by a single
backslash. The backslash character may be used for other escape sequences, which are summarized below:

* `\"` &ndash; double quote mark
* `\'` &ndash; single quote mark
* `\\` &ndash; backslash
* `\n` &ndash; newline
* `\r` &ndash; carriage return
* `\t` &ndash; horizontal tab
* `\v` &ndash; vertical tab
* `\f` &ndash; form feed
* `\a` &ndash; alert (BEL)
* `\b` &ndash; backspace
* `\x`_hh_ &ndash; hexadecimal byte
* `\u`_hhhh_ &ndash; 2-byte (hexadecimal) unicode codepoint
* `\U`_hhhhhhhh_ &ndash; 4-byte (hexadecimal) unicode codepoint
* `\ `<_newline_> &ndash; escaped newline in multiline string

### Symbols
Any other sequence of non-space, non-reserved, printable characters is a _symbol_.

### Comments
There are two types of comment in Beech: line comments and block comments. Line comments start with `#` and run to the end of the line (like Python comments). Block comments start with `~{` and end with `}~` and can be nested.
