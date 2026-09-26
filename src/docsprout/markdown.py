"""A deliberately small, safe Markdown renderer for documentation prose."""

from __future__ import annotations

from dataclasses import dataclass
import html
import re
from collections.abc import Callable

from .errors import DocSproutError
from .highlight import highlight_code, supports_language

LinkResolver = Callable[[str], str]
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE = re.compile(r"^```\s*([\w+-]*)\s*$")
LIST = re.compile(r"^\s*[-*+]\s+(.+)$")
ORDERED = re.compile(r"^\s*\d+[.)]\s+(.+)$")
LIST_ITEM = re.compile(r"^(?P<indent>\s*)(?:(?P<unordered>[-*+])|(?P<ordered>\d+[.)]))\s+(?P<text>.+)$")
TASK = re.compile(r"^\[([ xX])\]\s+(.+)$")
LINK = re.compile(r"\[([^]]+)]\(([^)]+)\)")
IMAGE = re.compile(r"!\[([^]]*)\]\(([^)]+)\)")
CODE = re.compile(r"`([^`]+)`")
STRIKE = re.compile(r"~~(.+?)~~")
HR = re.compile(r"^\s{0,3}(?:-[ \t]*){3,}$|^\s{0,3}(?:_[ \t]*){3,}$|^\s{0,3}(?:\*[ \t]*){3,}$")
INLINE_MATH = re.compile(r"(?<!\\)\$([^$\n]+)\$")
DEFINITION_DESCRIPTION = re.compile(r"^:\s+(.+)$")
PROTECTED_INLINE = re.compile(r"(`[^`]+`|(?<!\\)\$[^$\n]+\$|!?\[[^\]]*\]\([^)]*\))")
LINK_COMPONENTS = re.compile(r"(!?)\[([^\]]*)\]\(([^)]*)\)", re.DOTALL)
PROTECTED_SPAN = re.compile(r"`([^`]+)`|(?<!\\)\$([^$\n]+)\$")


def mask_protected_spans(line: str) -> str:
    """Mask inline code and math spans so link/image scans ignore them.

    Shared definition of protected inline contexts reused by the auditor.
    Spans are replaced with equal-length spaces to preserve positions.
    """

    return PROTECTED_SPAN.sub(lambda match: " " * len(match.group(0)), line)


@dataclass(frozen=True)
class RenderedMarkdown:
    html: str
    title: str
    headings: tuple[tuple[int, str, str], ...]
    text: str


def slugify(text: str) -> str:
    value = re.sub(r"[^\w\s-]", "", text.lower(), flags=re.UNICODE)
    return re.sub(r"[-\s]+", "-", value).strip("-") or "section"


def _plain(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[*_`~]+", "", value)).strip()


def _smart(value: str) -> str:
    value = value.replace("...", "…").replace("---", "—").replace("--", "–")
    output: list[str] = []
    for index, character in enumerate(value):
        previous = value[index - 1] if index else ""
        following = value[index + 1] if index + 1 < len(value) else ""
        if character == "'" and previous.isalnum() and following.isalnum():
            output.append("’")
        elif character in {'"', "'"}:
            opening = not previous or previous.isspace() or previous in "([{—–"
            if opening and following and not following.isspace():
                output.append("“" if character == '"' else "‘")
            else:
                output.append("”" if character == '"' else "’")
        else:
            output.append(character)
    return "".join(output)


def _typographic(value: str) -> str:
    parts = PROTECTED_INLINE.split(value)
    for index in range(0, len(parts), 2):
        parts[index] = _smart(parts[index])
    for index in range(1, len(parts), 2):
        link = LINK_COMPONENTS.fullmatch(parts[index])
        if link:
            parts[index] = f"{link.group(1)}[{_smart(link.group(2))}]({link.group(3)})"
    return "".join(parts)


def _inline(value: str, resolve: LinkResolver) -> str:
    # Protect inline code and math spans from every ordinary inline transform.
    # Code is literal code; math is TeX, not Markdown prose. The token is
    # deterministic per render, scoped to this call, and uses NUL sentinels
    # that ordinary prose never contains. The base is extended until it
    # cannot collide with the current input.
    base = "DOCSPROUT"
    while base in value:
        base += "X"
    contents: list[tuple[str, str]] = []

    def _stash(match: re.Match[str]) -> str:
        if match.group(1) is not None:
            contents.append(("code", match.group(1)))
        else:
            contents.append(("math", match.group(2) or ""))
        return f"\x00{base}{len(contents) - 1}\x00"

    working = PROTECTED_SPAN.sub(_stash, value)
    escaped = html.escape(_typographic(working), quote=False)
    escaped = IMAGE.sub(
        lambda match: f'<img src="{html.escape(resolve(html.unescape(match.group(2))), quote=True)}" alt="{html.escape(html.unescape(match.group(1)), quote=True)}">',
        escaped,
    )
    escaped = LINK.sub(lambda match: f'<a href="{html.escape(resolve(html.unescape(match.group(2))), quote=True)}">{match.group(1)}</a>', escaped)
    escaped = STRIKE.sub(r"<del>\1</del>", escaped)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*", r"<em>\1</em>", escaped)
    if contents:
        token = re.compile(r"\x00" + re.escape(base) + r"(\d+)\x00")

        def _restore(match: re.Match[str]) -> str:
            kind, raw = contents[int(match.group(1))]
            if kind == "code":
                return f"<code>{html.escape(raw, quote=False)}</code>"
            return f'<span class="math-inline" data-tex="{html.escape(raw, quote=True)}"></span>'

        escaped = token.sub(_restore, escaped)
    return escaped


def render_markdown(source: str, resolve_link: LinkResolver) -> RenderedMarkdown:
    lines = source.splitlines()
    output: list[str] = []
    plain: list[str] = []
    headings: list[tuple[int, str, str]] = []
    paragraph: list[str] = []
    seen: set[str] = set()
    index = 0

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(part.strip() for part in paragraph)
            output.append(f"<p>{_inline(text, resolve_link)}</p>")
            plain.append(_plain(text))
            paragraph.clear()

    def render_list(start: int, base_indent: int | None = None) -> tuple[str, int]:
        first = LIST_ITEM.match(lines[start])
        if not first:
            return "", start
        base_indent = base_indent if base_indent is not None else len(first.group("indent").expandtabs(4))
        ordered = first.group("ordered") is not None
        tag = "ol" if ordered else "ul"
        items: list[str] = []
        current = start
        while current < len(lines):
            match = LIST_ITEM.match(lines[current])
            if not match:
                break
            indent = len(match.group("indent").expandtabs(4))
            if indent < base_indent:
                break
            if indent > base_indent:
                if not items:
                    break
                nested, current = render_list(current, indent)
                items[-1] = items[-1].replace("</li>", f"{nested}</li>", 1)
                continue
            if (match.group("ordered") is not None) != ordered:
                break

            item = match.group("text").strip()
            current += 1
            parts = [item]
            while current < len(lines):
                continuation = lines[current]
                continuation_match = LIST_ITEM.match(continuation)
                if not continuation.strip() or not continuation[0].isspace():
                    break
                if continuation_match:
                    break
                parts.append(continuation.strip())
                current += 1
            item = " ".join(parts)
            task = TASK.match(item) if not ordered else None
            if task:
                complete = task.group(1).lower() == "x"
                state = "Complete" if complete else "Incomplete"
                items.append(f'<li><span class="task-list" role="img" aria-label="{state}">{"✓" if complete else "○"}</span>{_inline(task.group(2), resolve_link)}</li>')
                plain.append(_plain(task.group(2)))
            else:
                items.append(f"<li>{_inline(item, resolve_link)}</li>")
                plain.append(_plain(item))
        return f"<{tag}>{''.join(items)}</{tag}>", current

    while index < len(lines):
        line = lines[index]
        fence = FENCE.match(line)
        heading = HEADING.match(line)
        if fence:
            flush_paragraph()
            language = fence.group(1).lower() or "text"
            index += 1
            code: list[str] = []
            while index < len(lines) and not FENCE.match(lines[index]):
                code.append(lines[index])
                index += 1
            if index == len(lines):
                raise DocSproutError("Markdown: unclosed fenced code block")
            tex = "\n".join(code)
            if language == "math":
                output.append(f'<div class="math-display" data-tex="{html.escape(tex, quote=True)}"></div>')
            else:
                classes = f"language-{html.escape(language, quote=True)}"
                if supports_language(language):
                    classes += " syntax-highlight"
                output.append(f'<pre class="{classes}"><code>{highlight_code(tex, language)}</code></pre>')
            plain.extend(code)
        elif line.strip() == "$$":
            flush_paragraph()
            index += 1
            tex: list[str] = []
            while index < len(lines) and lines[index].strip() != "$$":
                tex.append(lines[index])
                index += 1
            if index == len(lines):
                raise DocSproutError("Markdown: unclosed display math block")
            value = "\n".join(tex)
            output.append(f'<div class="math-display" data-tex="{html.escape(value, quote=True)}"></div>')
            plain.extend(tex)
        elif heading:
            flush_paragraph()
            level, text = len(heading.group(1)), _plain(heading.group(2))
            identifier = slugify(text)
            if identifier in seen:
                suffix = 2
                while f"{identifier}-{suffix}" in seen:
                    suffix += 1
                identifier = f"{identifier}-{suffix}"
            seen.add(identifier)
            headings.append((level, text, identifier))
            output.append(f"<h{level} id=\"{identifier}\">{_inline(heading.group(2), resolve_link)}</h{level}>")
            plain.append(text)
        elif line.startswith("> [!") and "]" in line:
            flush_paragraph()
            kind, text = line[4:].split("]", 1)
            kind = kind.strip().lower()
            if kind not in {"note", "tip", "important", "warning"}:
                raise DocSproutError(f"Markdown: unsupported admonition {kind!r}")
            message = [text.strip()]
            index += 1
            while index < len(lines) and lines[index].startswith(">"):
                message.append(lines[index][1:].strip())
                index += 1
            body = " ".join(part for part in message if part)
            output.append(f'<aside class="admonition {kind}"><strong>{kind.title()}</strong><p>{_inline(body, resolve_link)}</p></aside>')
            plain.append(_plain(body))
            continue
        elif line.lstrip().startswith(">"):
            flush_paragraph()
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].lstrip().startswith(">"):
                stripped = lines[index].lstrip()
                content = stripped[1:]
                if content.startswith(" ") or content.startswith("\t"):
                    content = content[1:]
                quote_lines.append(content.rstrip())
                index += 1
            paragraphs: list[list[str]] = [[]]
            for quote_line in quote_lines:
                if quote_line.strip():
                    paragraphs[-1].append(quote_line.strip())
                elif paragraphs[-1]:
                    paragraphs.append([])
            paragraphs = [part for part in paragraphs if part]
            if paragraphs:
                body_html = "".join(f"<p>{_inline(' '.join(part), resolve_link)}</p>" for part in paragraphs)
                for part in paragraphs:
                    plain.append(_plain(" ".join(part)))
            else:
                body_html = ""
            output.append(f"<blockquote>{body_html}</blockquote>")
            continue
        elif HR.match(line):
            flush_paragraph()
            output.append("<hr>")
        elif line.strip() and index + 1 < len(lines) and DEFINITION_DESCRIPTION.match(lines[index + 1]):
            flush_paragraph()
            items: list[str] = []
            while index + 1 < len(lines) and lines[index].strip():
                description = DEFINITION_DESCRIPTION.match(lines[index + 1])
                if not description:
                    break
                term = lines[index]
                value = description.group(1)
                items.append(f"<dt>{_inline(term.strip(), resolve_link)}</dt><dd>{_inline(value, resolve_link)}</dd>")
                plain.extend((_plain(term), _plain(value)))
                index += 2
            output.append(f"<dl>{''.join(items)}</dl>")
            continue
        elif LIST.match(line) or ORDERED.match(line):
            flush_paragraph()
            list_html, index = render_list(index)
            output.append(list_html)
            continue
        elif "|" in line and index + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}", lines[index + 1]):
            flush_paragraph()
            headers = [cell.strip() for cell in line.strip().strip("|").split("|")]
            index += 2
            rows: list[list[str]] = []
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                rows.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
                index += 1
            header_html = "".join(f"<th>{_inline(cell, resolve_link)}</th>" for cell in headers)
            body_html = "".join("<tr>" + "".join(f"<td>{_inline(cell, resolve_link)}</td>" for cell in row) + "</tr>" for row in rows)
            output.append(f'<div class="table-scroll"><table><thead><tr>{header_html}</tr></thead><tbody>{body_html}</tbody></table></div>')
            plain.extend(headers)
            plain.extend(cell for row in rows for cell in row)
            continue
        elif not line.strip():
            flush_paragraph()
        else:
            paragraph.append(line)
        index += 1
    flush_paragraph()
    title = next((text for level, text, _ in headings if level == 1), "Documentation")
    return RenderedMarkdown("\n".join(output), title, tuple(headings), re.sub(r"\s+", " ", " ".join(plain)).strip())
