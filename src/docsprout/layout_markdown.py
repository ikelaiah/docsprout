"""Parse the deliberately small Markdown navigation outline."""

from __future__ import annotations

import re
from pathlib import Path

from .config import safe_document_path
from .errors import DocSproutError


_PAGE = re.compile(r"^- \[((?:\\.|[^\\\]])+)\]\((<[^<>]+>|(?:\\.|[^\\)])+)\)$")
_ESCAPE = re.compile(r"\\([\\\[\]()])")
_GROUP_ATTRIBUTE = re.compile(r"^(.*?)\s+\{([^{}]+)\}$")


def read_markdown_layout(path: Path) -> dict:
    """Turn a navigation outline into schema-1 data for shared validation."""
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as error:
        raise DocSproutError(f"{path}: cannot read layout: {error}") from error

    def fail(number: int, message: str) -> None:
        raise DocSproutError(f"{path}:{number}: {message}")

    metadata: dict[str, str] = {}
    metadata_lines: dict[str, int] = {}
    navigation: list[dict] = []
    section: dict | None = None
    group: dict | None = None
    section_line = 0
    group_line = 0
    seen_pages: set[tuple[str, str]] = set()
    listed_sources: set[tuple[str, str]] = set()
    started = False

    for number, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line:
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent not in {0, 2} or "\t" in raw[:len(raw) - len(raw.lstrip())]:
            fail(number, "use no indentation for sections and pages, or two spaces for group pages")
        if indent and not line.startswith("- "):
            fail(number, "only group page links may be indented")
        if not started and ":" in line and not line.startswith(("#", "- ")):
            key, value = (part.strip() for part in line.split(":", 1))
            if key not in {"Layout-Version", "Home", "Unlisted"}:
                fail(number, f"unsupported layout setting {key!r}")
            if key in metadata:
                fail(number, f"duplicate layout setting {key!r}")
            if not value:
                fail(number, f"layout setting {key!r} needs a value")
            metadata[key] = value
            metadata_lines[key] = number
            continue
        started = True
        if line.startswith("###"):
            fail(number, "unsupported heading depth; use # sections and ## groups")
        if line.startswith("# "):
            if group is not None and not group["pages"]:
                fail(group_line, f"navigation group {group['title']!r} needs pages")
            if section is not None and not section["pages"]:
                fail(section_line, f"navigation section {section['title']!r} needs pages")
            title = line[2:].strip()
            if not title or "{" in title or "}" in title:
                fail(number, "section needs a plain, non-empty title")
            section = {"title": title, "pages": []}
            section_line = number
            navigation.append(section)
            group = None
            continue
        if line.startswith("## "):
            if section is None:
                fail(number, "group needs a preceding # section")
            if group is not None and not group["pages"]:
                fail(group_line, f"navigation group {group['title']!r} needs pages")
            title = line[3:].strip()
            expanded = False
            attribute = _GROUP_ATTRIBUTE.fullmatch(title)
            if attribute:
                title, option = attribute.groups()
                if option not in {"expanded", "expanded=true", "expanded=false"}:
                    fail(number, f"unsupported group attribute {{{option}}}; use {{expanded=true}}")
                expanded = option != "expanded=false"
            elif "{" in title or "}" in title:
                fail(number, "unsupported group attribute; use {expanded=true}")
            if not title.strip():
                fail(number, "group needs a non-empty title")
            group = {"title": title.strip(), "pages": [], "expanded": expanded}
            group_line = number
            section["pages"].append(group)
            continue
        match = _PAGE.fullmatch(line)
        if match:
            if section is None:
                fail(number, "page needs a preceding # section")
            if indent == 2 and group is None:
                fail(number, "indented page needs a preceding ## group")
            if indent == 0 and group is not None:
                if not group["pages"]:
                    fail(group_line, f"navigation group {group['title']!r} needs pages")
                group = None
            title = _ESCAPE.sub(r"\1", match.group(1))
            target = match.group(2)
            target = target[1:-1] if target.startswith("<") else _ESCAPE.sub(r"\1", target)
            if not title.strip():
                fail(number, "page needs a non-empty title")
            if target == "../README.md":
                entry = {"title": title, "path": "README.md", "source": "root"}
            else:
                document = safe_document_path(target, f"{path}:{number}")
                if document == "layout.md":
                    fail(number, "layout.md is configuration and cannot be a navigation page")
                entry = {"title": title, "path": document}
            source_path = path.parent.parent / "README.md" if entry.get("source") == "root" else path.parent / entry["path"]
            if not source_path.is_file():
                fail(number, f"navigation page {target!r} does not exist")
            identity = (entry.get("source", "docs"), entry["path"])
            if identity in seen_pages:
                fail(number, f"navigation page {target!r} appears more than once")
            seen_pages.add(identity)
            listed_sources.add(identity)
            (group if indent else section)["pages"].append(entry)
            continue
        fail(number, "unsupported outline line; use a # section, ## group, or - [Title](path.md) page")

    if group is not None and not group["pages"]:
        fail(group_line, f"navigation group {group['title']!r} needs pages")
    if section is not None and not section["pages"]:
        fail(section_line, f"navigation section {section['title']!r} needs pages")
    if metadata.get("Layout-Version") != "1":
        fail(metadata_lines.get("Layout-Version", 1), "Layout-Version: 1 is required")
    layout: dict = {"schema_version": 1, "navigation": navigation}
    if "Home" in metadata:
        home = metadata["Home"]
        if home == "../README.md":
            layout["home"] = {"path": "README.md", "source": "root"}
        else:
            layout["home"] = {"path": safe_document_path(home, f"{path}:{metadata_lines['Home']}")}
        home_entry = layout["home"]
        if (home_entry.get("source", "docs"), home_entry["path"]) not in listed_sources:
            fail(metadata_lines["Home"], f"home {home!r} must name a listed navigation page")
    if "Unlisted" in metadata:
        if metadata["Unlisted"] not in {"error", "exclude"}:
            fail(metadata_lines["Unlisted"], "Unlisted must be 'error' or 'exclude'")
        layout["unlisted"] = metadata["Unlisted"]
    return layout
