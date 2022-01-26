# Beech
A simple tree-based language.

## Syntax
The syntax of Beech is based primarily around the tree data type. Beech also provides literals for strings and numbers.

### Tree Literals
An _unordered_ tree is delimited by braces and has zero or more key-value pairs, with each key unique. The key and value are separated by whitespace, as are the key-value pairs themselves:
`{` _key1_ &nbsp;_value1_ &nbsp;_key2_ &nbsp;_value2_ &nbsp;&hellip; `}`.

An _ordered_ tree is delimited by square brackets. Structure is implied by the order it is written in, so keys may be duplicated:
`[` _key_ &nbsp;_value1_ &nbsp;_key_ &nbsp;_value2_ &nbsp;&hellip; `]`.

A third type of tree is a _list_, which is delimited by parentheses. This is syntactic sugar for an unordered tree where the keys are 1, &hellip;, n for n items:
`(` _value1_ &nbsp;_value2_&nbsp;&nbsp;&hellip; `)`.

### String Literals
A string literal is delimited by matching quote marks (either double `"` or single `'`). It may contain any ASCII printable character except for the quote mark matching the delimiters and the backslash character. These characters may be added to the string by escaping them with a backslash `\ `. The backslash can also be used in other escape sequences, which are listed below:

* `\"` &ndash; double quote mark
* `\'` &ndash; single quote mark
* `\\` &ndash; backslash
* `\n` &ndash; newline
* `\r` &ndash; carriage return
* `\t` &ndash; tab
* `\0` &ndash; NUL byte

### Numeric Literals
Beech supports integer and floating point numeric types.

An integer literal is a sequence of one or more of the digits 0&ndash;9. Hexadecimal integer literals may be prefixed with `0x` and contain the digits 0&ndash;9 and the characters a&ndash;f and A&ndash;F (case may be freely mixed inside the literal).

A floating point literal may contain the digits 0&ndash;9 and up to 1 decimal separator (`.`). The decimal point may appear at the beginning or end of the literal, or in between digits. An 'exponent part' may also be included, which appears at the end of the literal. The exponent part starts with the letter `e` (case-insensitive), followed by an integer literal.

Both integer and floating point literals may be signed, denoted by a leading `+` or `-` sign.
