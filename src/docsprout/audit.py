"""Read-only publication-readiness diagnostics for DocSprout projects."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import posixpath
import re
from urllib.parse import urlsplit

from .config import load_config, page_source_path, page_source_reference
from .markdown import HEADING, render_markdown, slugify


IMAGE = re.compile(r"!\[([^]]*)\]\(([^)]+)\)")
LINK = re.compile(r"(?<!!)\[([^]]+)\]\(([^)]+)\)")
FENCE = re.compile(r"^\s*```")
SAFE_EXTERNAL_SCHEMES = {"http", "https", "mailto"}


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    file: str
    line: int
    message: str
    detail: str
    target: str | None = None


@dataclass(frozen=True)
class AuditResult:
    pages: int
    findings: tuple[Finding, ...]
    excluded_documents: int = 0

    @property
    def errors(self) -> int:
        return sum(finding.severity == "error" for finding in self.findings)

    @property
    def warnings(self) -> int:
        return sum(finding.severity == "warning" for finding in self.findings)


@dataclass(frozen=True)
class _AuditPage:
    path: str
    source: str
    headings: tuple[tuple[int, str, str], ...]
    text: str


def _load_pages(root: Path) -> tuple[tuple[_AuditPage, ...], int]:
    config = load_config(root)
    pages: list[_AuditPage] = []
    for page in config.pages:
        source = page_source_path(root, page).read_text(encoding="utf-8")
        pages.append(_AuditPage(page.path, page_source_reference(page), render_markdown(source, lambda target: target).headings, source))
    return tuple(pages), len(config.excluded_documents)


def _finding(code: str, severity: str, page: _AuditPage, line: int, message: str, detail: str, target: str | None = None) -> Finding:
    return Finding(code, severity, page.source, line, message, detail, target)


def _is_external(target: str) -> bool:
    return urlsplit(target).scheme.lower() in SAFE_EXTERNAL_SCHEMES


def _source_target(page: _AuditPage, document: str) -> str:
    return posixpath.normpath(posixpath.join(posixpath.dirname(page.source), document))


def _is_safe_document_reference(reference: str) -> bool:
    return reference == "README.md" or reference.startswith("docs/")


def _is_safe_local_file(root: Path, reference: str) -> bool:
    try:
        candidate = (root / Path(reference)).resolve()
    except OSError:
        return False
    return candidate.is_relative_to(root) and candidate.is_file()


def _audit_link(page: _AuditPage, line: int, target: str, pages: dict[str, _AuditPage], root: Path) -> Finding | None:
    parsed = urlsplit(target)
    if _is_external(target):
        return None
    if parsed.scheme or target.startswith("/"):
        return _finding("DK005", "error", page, line, "Unsafe local link", "Use an https, http or mailto URL, or a repository-local documentation path.", target)
    document, marker, fragment = target.partition("#")
    if not document and marker:
        requested_source = page.source
    elif document.lower().endswith(".md"):
        requested_source = _source_target(page, document)
    else:
        return None
    if not _is_safe_document_reference(requested_source):
        return _finding("DK005", "error", page, line, "Local link escapes documentation paths", "Use a published docs page or the repository README.", target)
    target_page = pages.get(requested_source)
    if target_page is None:
        if (root / Path(requested_source)).is_file():
            return _finding("DK002", "error", page, line, "Link targets unpublished Markdown", "The Markdown file exists but is not in layout.json navigation.", target)
        return _finding("DK001", "error", page, line, "Broken local page link", "The target is not part of the published documentation.", target)
    if marker and fragment not in {identifier for _level, _text, identifier in target_page.headings}:
        return _finding("DK003", "error", page, line, "Broken heading anchor", "The published page does not contain that heading anchor.", target)
    return None


def _audit_image(page: _AuditPage, line: int, alt: str, target: str, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not alt.strip():
        findings.append(_finding("DK101", "warning", page, line, "Image has no alternative text", "Add concise text that conveys the image's meaning.", target))
    if _is_external(target):
        return findings
    parsed = urlsplit(target)
    if parsed.scheme or target.startswith("/"):
        findings.append(_finding("DK005", "error", page, line, "Unsafe local asset link", "Use an https, http or mailto URL, or a repository-local documentation path.", target))
        return findings
    asset = target.partition("#")[0]
    if not asset:
        return findings
    requested_source = _source_target(page, asset)
    if not _is_safe_document_reference(requested_source) or not _is_safe_local_file(root, requested_source):
        findings.append(_finding("DK004", "error", page, line, "Missing local image or asset", "Add the asset under the documentation content path or correct the reference.", target))
    return findings


def _audit_page(page: _AuditPage, pages: dict[str, _AuditPage], root: Path) -> list[Finding]:
    findings: list[Finding] = []
    structural_findings: list[Finding] = []
    inside_fence = False
    previous_level: int | None = None
    anchors: set[str] = set()
    heading_lines: list[int] = []
    for line_number, source_line in enumerate(page.text.splitlines(), start=1):
        if FENCE.match(source_line):
            inside_fence = not inside_fence
        elif not inside_fence and HEADING.match(source_line):
            heading_lines.append(line_number)
    for (level, text, _identifier), line_number in zip(page.headings, heading_lines):
        anchor = slugify(text)
        if anchor in anchors:
            structural_findings.append(_finding("DK103", "warning", page, line_number, "Duplicate heading anchor", "Rename one heading. Anchors that share the same text receive a numeric suffix and stay ambiguous to link.", anchor))
        anchors.add(anchor)
        if previous_level is not None and level > previous_level + 1:
            structural_findings.append(_finding("DK102", "warning", page, line_number, f"Heading level jumps from H{previous_level} to H{level}", "Use an intermediate heading level when it represents document structure."))
        previous_level = level
    inside_fence = False
    for line_number, source_line in enumerate(page.text.splitlines(), start=1):
        if FENCE.match(source_line):
            inside_fence = not inside_fence
            continue
        if inside_fence:
            continue
        matches = [(match.start(), "image", match) for match in IMAGE.finditer(source_line)]
        matches.extend((match.start(), "link", match) for match in LINK.finditer(source_line))
        for _position, kind, match in sorted(matches, key=lambda item: item[0]):
            if kind == "image":
                findings.extend(_audit_image(page, line_number, match.group(1), match.group(2).strip(), root))
            else:
                finding = _audit_link(page, line_number, match.group(2).strip(), pages, root)
                if finding is not None:
                    findings.append(finding)
    findings.extend(structural_findings)
    return findings


def audit_project(root: Path) -> AuditResult:
    """Audit the configured public pages without modifying the project."""
    root = root.resolve()
    page_list, excluded = _load_pages(root)
    pages = {page.source: page for page in page_list}
    findings = tuple(finding for page in page_list for finding in _audit_page(page, pages, root))
    return AuditResult(pages=len(page_list), findings=findings, excluded_documents=excluded)


def format_text(result: AuditResult) -> str:
    """Return concise, stable human-readable audit output."""
    lines = ["DocSprout documentation audit", ""]
    for severity, label in (("error", "ERRORS"), ("warning", "WARNINGS")):
        findings = [finding for finding in result.findings if finding.severity == severity]
        if not findings:
            continue
        lines.extend((label, ""))
        for finding in findings:
            location = f"{finding.file}:{finding.line}" if finding.line else finding.file
            target = f": {finding.target}" if finding.target else ""
            lines.extend((f"{finding.code} {location}", f"{finding.message}{target}", finding.detail, ""))
    lines.extend(("Summary", f"  Pages audited: {result.pages}", f"  Errors: {result.errors}", f"  Warnings: {result.warnings}"))
    if result.excluded_documents:
        lines.append(f"  Unpublished Markdown files: {result.excluded_documents}")
    lines.extend(("", "Ready to publish." if not result.errors else "Audit found publication problems.", "External URLs were not network-checked."))
    return "\n".join(lines)


def format_json(result: AuditResult) -> str:
    """Return deterministic machine-readable audit diagnostics."""
    return json.dumps({
        "schema_version": 1,
        "pages": result.pages,
        "errors": result.errors,
        "warnings": result.warnings,
        "findings": [
            {
                "code": finding.code,
                "severity": finding.severity,
                "file": finding.file,
                "line": finding.line,
                "message": finding.message,
                **({"target": finding.target} if finding.target is not None else {}),
            }
            for finding in result.findings
        ],
    }, ensure_ascii=False, indent=2)
