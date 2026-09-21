"""Small, offline-safe syntax highlighting for fenced documentation code."""

from __future__ import annotations

import html
import re


ALIASES = {"fpc": "pascal", "freepascal": "pascal", "py": "python", "sh": "bash", "shell": "bash", "yml": "yaml", "md": "markdown"}
KEYWORDS = {
    "pascal": {"program", "unit", "interface", "implementation", "uses", "var", "const", "type", "procedure", "function", "begin", "end", "if", "then", "else", "for", "to", "downto", "do", "while", "repeat", "until", "case", "of", "record", "class", "try", "except", "finally", "raise", "with"},
    "python": {"as", "assert", "async", "await", "break", "class", "continue", "def", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal", "pass", "raise", "return", "try", "while", "with", "yield"},
    "bash": {"case", "do", "done", "elif", "else", "esac", "fi", "for", "function", "if", "in", "select", "then", "until", "while"},
}
FUNCTIONS = {"pascal": {"readln", "writeln", "write", "length", "setlength", "assigned", "freeandnil"}, "python": {"print", "len", "range", "open", "str", "int", "list", "dict"}, "bash": {"echo", "printf", "cd", "read", "export"}}
TOKEN_PATTERNS = {
    "pascal": re.compile(r"(?P<comment>//[^\n]*|\{.*?\}|\(\*.*?\*\))|(?P<string>'(?:''|[^'])*')|(?P<number>\b\d+(?:\.\d+)?\b)|(?P<word>\b[A-Za-z_]\w*\b)", re.DOTALL),
    "python": re.compile(r"(?P<comment>#[^\n]*)|(?P<string>'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\")|(?P<number>\b\d+(?:\.\d+)?\b)|(?P<word>\b[A-Za-z_]\w*\b)"),
    "bash": re.compile(r"(?P<comment>#[^\n]*)|(?P<string>'[^']*'|\"(?:\\.|[^\"\\])*\")|(?P<number>\b\d+(?:\.\d+)?\b)|(?P<word>\b[A-Za-z_]\w*\b)"),
    "yaml": re.compile(r"(?P<comment>#[^\n]*)|(?P<string>'[^']*'|\"(?:\\.|[^\"\\])*\")|(?P<number>\b\d+(?:\.\d+)?\b)|(?P<word>\b[A-Za-z_]\w*\b)"),
    "markdown": re.compile(r"(?P<heading>^#{1,6}\s.*$)|(?P<code>`[^`]+`)|(?P<string>\[[^]]+]\([^)]*\))", re.MULTILINE),
}
JSON_TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|\b(?:true|false|null)\b|-?\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b')


def normalise_language(language: str) -> str:
    return ALIASES.get(language.lower(), language.lower())


def supports_language(language: str) -> bool:
    return normalise_language(language) in {"json", *TOKEN_PATTERNS}


def _span(kind: str, value: str) -> str:
    return f'<span class="tok-{kind}">{html.escape(value)}</span>'


def _highlight_json(source: str) -> str:
    output: list[str] = []
    end = 0
    for match in JSON_TOKEN.finditer(source):
        output.append(html.escape(source[end:match.start()]))
        value = match.group(0)
        if value.startswith('"'):
            kind = "property" if source[match.end():].lstrip().startswith(":") else "string"
        elif value in {"true", "false"}:
            kind = "boolean"
        elif value == "null":
            kind = "constant"
        else:
            kind = "number"
        output.append(_span(kind, value))
        end = match.end()
    output.append(html.escape(source[end:]))
    return "".join(output)


def highlight_code(source: str, language: str) -> str:
    language = normalise_language(language)
    if language == "json":
        return _highlight_json(source)
    pattern = TOKEN_PATTERNS.get(language)
    if pattern is None:
        return html.escape(source)
    output: list[str] = []
    end = 0
    for match in pattern.finditer(source):
        output.append(html.escape(source[end:match.start()]))
        kind = match.lastgroup or "text"
        value = match.group(0)
        if kind == "word":
            lowered = value.lower()
            if language == "yaml" and source[match.end():].lstrip().startswith(":"):
                kind = "property"
            elif lowered in {"true", "false", "yes", "no"}:
                kind = "boolean"
            elif lowered in {"none", "null"}:
                kind = "constant"
            elif lowered in KEYWORDS.get(language, set()):
                kind = "keyword"
            elif lowered in FUNCTIONS.get(language, set()):
                kind = "function"
        output.append(_span(kind, value))
        end = match.end()
    output.append(html.escape(source[end:]))
    return "".join(output)
