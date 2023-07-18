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
* `\t` &ndash; horizontal tab
* `\v` &ndash; vertical tab
* `\f` &ndash; form feed
* `\a` &ndash; alert (BEL)
* `\b` &ndash; backspace
* `\x`_hh_ &ndash; hexadecimal byte
* `\u`_hhhh_ &ndash; 2-byte (hexadecimal) unicode codepoint
* `\U`_hhhhhhhh_ &ndash; 4-byte (hexadecimal) unicode codepoint

### Symbols
Any other sequence of non-space, non-reserved, printable characters is a _symbol_.

### Comments
There are two types of comment in Beech: line comments and block comments. Line comments start with `#` and run to the end of the line (like Python comments). Block comments start with `~{` and end with `}~` and can be nested.
