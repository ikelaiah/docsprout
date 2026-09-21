"""Build a complete static documentation site from a project source tree."""

from __future__ import annotations

from dataclasses import dataclass
import html
import json
from pathlib import Path
import posixpath
import re
import shutil
from urllib.parse import urlsplit

from .assets import MATH_JS, SITE_CSS, SITE_JS
from .config import load_config, page_source_path, page_source_reference
from .errors import DocSproutError
from .markdown import render_markdown
from .models import Page
from .safety import prepare_output


DEFAULT_CAPABILITIES = (
    ("Offline", "Local assets, no CDN."),
    ("Versioned", "Release history stays browsable."),
    ("KaTeX", "Mathematics renders locally."),
    ("Pascal-ready", "Made for FP and Lazarus docs."),
)
INITIAL_INTRODUCTION = re.compile(r"^(<h1\b[^>]*>.*?</h1>\s*)<p>.*?</p>\s*", re.DOTALL)


@dataclass(frozen=True)
class BuildResult:
    page_count: int
    section_count: int
    legacy: bool
    home_document: str
    excluded_count: int = 0


def _route(document: str, home: str) -> str:
    if document == home:
        return "index.html"
    # Keep docs/index.md reachable whenever a different page owns the site's
    # index route, including an explicit docs page or repository-root README.
    if document == "index.md" and home != "index.md":
        return "docs-index.html"
    return str(Path(document).with_suffix(".html").as_posix())


def _safe_url(target: str) -> str:
    parsed = urlsplit(target)
    if parsed.scheme and parsed.scheme.lower() not in {"https", "http", "mailto"}:
        raise DocSproutError(f"Markdown: unsafe URL scheme in {target!r}")
    if not parsed.scheme and target.startswith("/"):
        raise DocSproutError(f"Markdown: unsafe local link {target!r}")
    return target


def _relative(source_route: str, target_route: str) -> str:
    return posixpath.relpath(target_route, posixpath.dirname(source_route) or ".")


def _page_navigation(*, page: Page, config, current_route: str) -> str:
    position = config.pages.index(page)
    links: list[str] = []
    for label, item in (("Previous", config.pages[position - 1] if position else None), ("Next", config.pages[position + 1] if position + 1 < len(config.pages) else None)):
        if item is not None:
            href = html.escape(_relative(current_route, _route(item.path, config.home_document)), quote=True)
            links.append(f'<a class="page-{label.lower()}" href="{href}"><small>{label}</small><span>{html.escape(item.title)}</span></a>')
    return f'<nav class="page-navigation" aria-label="Page navigation">{"".join(links)}</nav>' if links else ""


def _shell(*, body: str, headings: tuple[tuple[int, str, str], ...], page: Page, config, current_route: str, version_options: str, banner: str | None, logo: str | None, release: str, custom_css: bool = False) -> str:
    navigation_sections: list[str] = []
    for section in dict.fromkeys(item.section for item in config.pages):
        section_links: list[str] = []
        for item in config.pages:
            if item.section != section:
                continue
            is_current = item.path == page.path
            active_class = "active" if is_current else ""
            aria_current = ' aria-current="page"' if is_current else ""
            href = html.escape(_relative(current_route, _route(item.path, config.home_document)), quote=True)
            section_links.append(
                f'<a class="{active_class}" href="{href}"{aria_current}>{html.escape(item.title)}</a>'
            )
        navigation_sections.append(f'<h2>{html.escape(section)}</h2>{"".join(section_links)}')
    nav = "".join(navigation_sections)
    banner_html = f'<img class="banner" src="{html.escape(banner, quote=True)}" alt="{html.escape(config.banner_alt or "", quote=True)}">' if banner else ""
    style = f"--dk-accent:{config.accent};--dk-accent-secondary:{config.accent_secondary}"
    brand_mark = '<svg class="brand-mark" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M3 1.5h6l4 4v9H3zM9 1.5v4h4M5.5 9h5M5.5 11.5h4"/></svg>'
    brand_identity = f'<img class="brand-logo" src="{html.escape(_relative(current_route, logo), quote=True)}" alt="" aria-hidden="true">' if logo else brand_mark
    if page.path == config.home_document and not config.homepage.show_introduction:
        body = INITIAL_INTRODUCTION.sub(r"\1", body)
    cards = config.homepage.capabilities if config.homepage.capabilities is not None else DEFAULT_CAPABILITIES
    capability_strip = ""
    if page.path == config.home_document and config.homepage.show_capabilities and cards:
        card_html = "".join(
            f"<li><strong>{html.escape(title)}</strong><span>{html.escape(description)}</span></li>"
            for title, description in cards
        )
        capability_strip = f'<ul class="capability-strip" data-card-count="{len(cards)}" aria-label="{html.escape(config.name)} capabilities">{card_html}</ul>'
    if capability_strip:
        title_end = body.find("</h1>")
        insert_at = title_end + len("</h1>") if title_end >= 0 else 0
        paragraph_start = body.find("<p>", insert_at)
        if paragraph_start >= 0 and not body[insert_at:paragraph_start].strip():
            insert_at = body.find("</p>", paragraph_start) + len("</p>")
        body = body[:insert_at] + capability_strip + body[insert_at:]
    toc_links = "".join(
        f'<a class="toc-level-{level}" href="#{html.escape(identifier, quote=True)}">{html.escape(text)}</a>'
        for level, text, identifier in headings if level > 1
    )
    toc = f'<p class="toc-title">On this page</p>{toc_links}' if toc_links else '<p class="toc-title">Documentation</p><p class="toc-empty-copy">Browse the sections in the navigation.</p>'
    page_navigation = _page_navigation(page=page, config=config, current_route=current_route)
    footer_links = "".join(f'<a href="{html.escape(url, quote=True)}">{html.escape(label)}</a>' for label, url in config.project_links)
    footer = f'<footer class="site-footer"><span>{html.escape(config.footer or config.name)}</span>{footer_links}</footer>' if config.footer or footer_links else ""
    release_context = f'<aside class="release-context" aria-label="Release context"><strong>Release</strong><span>{html.escape(release)}</span></aside>' if page.path == config.home_document and config.homepage.show_release_context else ""
    header_controls = f'''<div class="header-controls" aria-label="Site controls"><label class="header-control"><span>Version</span><select id="version-select" aria-label="Documentation version">{version_options}</select></label><label class="header-control"><span>Style</span><select id="visual-theme" aria-label="Documentation visual theme"><option value="classic">Classic</option><option value="paper">Paper</option><option value="midnight">Midnight</option></select></label><label class="header-control"><span>Mode</span><select id="theme-select" aria-label="Colour theme"><option value="system">System</option><option value="light">Light</option><option value="dark">Dark</option></select></label></div>'''
    homepage = page.path == config.home_document
    main_context = ' data-homepage="true"' if homepage else ' data-homepage="false"'
    theme_bootstrap = """<script>try{const root=document.documentElement,readStored=(primary,legacy)=>{const value=localStorage.getItem(primary);if(value!==null)return value;const previous=localStorage.getItem(legacy);if(previous!==null){localStorage.setItem(primary,previous);localStorage.removeItem(legacy);return previous}return null},theme=readStored('docsprout-theme','dockit-fp-theme'),visualTheme=readStored('docsprout-visual-theme','dockit-fp-visual-theme');if(theme==='light'||theme==='dark')root.dataset.theme=theme;if(['classic','paper','midnight'].includes(visualTheme))root.dataset.visualTheme=visualTheme}catch(_){}</script>"""
    custom_css_link = f'<link rel="stylesheet" href="{html.escape(_relative(current_route, "assets/custom.css"), quote=True)}">' if custom_css else ""
    return f'''<!doctype html><html lang="en" data-visual-theme="{html.escape(config.theme_style, quote=True)}" data-content-width="{html.escape(config.content_width, quote=True)}" style="{style}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{html.escape(config.description, quote=True)}"><title>{html.escape(page.title)} — {html.escape(config.name)}</title><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath fill='%237c3aed' d='M3 1.5h6l4 4v9H3zM9 1.5v4h4M5.5 9h5M5.5 11.5h4'/%3E%3C/svg%3E">{theme_bootstrap}<link rel="stylesheet" href="{html.escape(_relative(current_route, 'assets/site.css'), quote=True)}"><link rel="stylesheet" href="{html.escape(_relative(current_route, 'assets/katex/katex.min.css'), quote=True)}">{custom_css_link}</head><body><div class="reading-progress" aria-hidden="true"><span></span></div><header class="site-header"><div class="topbar"><a class="brand" href="{html.escape(_relative(current_route, 'index.html'), quote=True)}">{brand_identity}<span>{html.escape(config.name)}</span> <em>docs</em></a><div class="search-control"><input id="search" type="search" placeholder="Search docs, commands, and versions" aria-label="Search documentation, commands, and versions" aria-controls="search-results" aria-describedby="search-help" aria-expanded="false" autocomplete="off" data-search-index="{html.escape(_relative(current_route, 'search-index.json'), quote=True)}"><kbd aria-hidden="true" title="Press / to search">/</kbd><span id="search-help" class="visually-hidden">Type to search. Use the arrow keys to move through results, Enter to open, and Escape to close.</span></div>{header_controls}</div><div id="search-results" class="search-results" role="region" aria-label="Search results" aria-live="polite" hidden></div></header><details class="mobile-nav"><summary>Browse documentation</summary>{nav}</details><div class="shell"><nav class="sidebar" aria-label="Documentation navigation">{nav}</nav><main class="prose" id="content"{main_context}>{banner_html}{release_context}{body}{page_navigation}</main><aside class="toc" aria-label="On this page">{toc}</aside></div>{footer}<script src="{html.escape(_relative(current_route, 'assets/katex/katex.min.js'), quote=True)}"></script><script src="{html.escape(_relative(current_route, 'assets/math.js'), quote=True)}"></script><script src="{html.escape(_relative(current_route, 'assets/site.js'), quote=True)}"></script></body></html>'''


def detect_route_collisions(pages: tuple[Page, ...], home: str) -> None:
    """Reject documented pages whose generated routes would overwrite each other.

    Exact collisions are deterministic on every platform. Case-insensitive
    collisions are also rejected because supported hosts include
    case-insensitive filesystems; a site that builds on Linux must not
    silently break when deployed to GitHub Pages or a Windows/macOS host.
    """
    owners: dict[str, str] = {}
    for page in pages:
        route = _route(page.path, home)
        for key in (route, route.casefold()):
            owner = owners.get(key)
            if owner is not None and owner != page.path:
                raise DocSproutError(
                    f"Generated route collision: {route!r} is produced by both {owner!r} and {page.path!r}. "
                    "Rename or move one of the listed Markdown documents so every published route is unique."
                )
            owners[key] = page.path


def build_site(
    *, root: Path, output: Path, release: str, versions: tuple[tuple[str, str], ...] = (),
    require_listed_documents: bool = True,
) -> BuildResult:
    """Build one release. `root` is never used as an output location."""
    root, output = root.resolve(), output.resolve()
    config = load_config(root, require_listed_documents=require_listed_documents)
    docs = root / "docs"
    routes = {item.path: _route(item.path, config.home_document) for item in config.pages}
    detect_route_collisions(config.pages, config.home_document)
    prepare_output(output)
    assets = output / "assets"
    assets.mkdir()
    (assets / "site.css").write_text(SITE_CSS, encoding="utf-8")
    (assets / "site.js").write_text(SITE_JS, encoding="utf-8")
    (assets / "math.js").write_text(MATH_JS, encoding="utf-8")
    shutil.copytree(Path(__file__).parent / "vendor" / "katex", assets / "katex")
    banner = None
    if config.banner:
        suffix = Path(config.banner).suffix.lower()
        banner = f"assets/banner{suffix}"
        shutil.copyfile(root / config.banner, output / banner)
    logo = None
    if config.logo:
        suffix = Path(config.logo).suffix.lower()
        logo = f"assets/logo{suffix}"
        shutil.copyfile(root / config.logo, output / logo)
    custom_css_route = None
    if config.custom_css:
        custom_css_route = "assets/custom.css"
        shutil.copyfile(root / config.custom_css, output / custom_css_route)
    source_documents = {page_source_reference(page): page.path for page in config.pages}
    content_assets: dict[str, str] = {}
    anchors = {
        page.path: {identifier for _level, _text, identifier in render_markdown(page_source_path(root, page).read_text(encoding="utf-8"), lambda target: target).headings}
        for page in config.pages
    }
    entries: list[dict[str, str]] = []
    for page in config.pages:
        source = page_source_path(root, page).read_text(encoding="utf-8")
        current_route = routes[page.path]
        def resolve(target: str) -> str:
            target = _safe_url(target)
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                return target
            document, marker, fragment = target.partition("#")
            current_source = page_source_reference(page)
            requested_source = posixpath.normpath(posixpath.join(posixpath.dirname(current_source), document)) if document else current_source
            if requested_source == ".." or requested_source.startswith("../"):
                raise DocSproutError(f"Markdown: unsafe local link {target!r}")
            requested = source_documents.get(requested_source)
            if requested not in routes:
                if requested_source == "README.md" or not requested_source.startswith("docs/"):
                    raise DocSproutError(f"Markdown: unsafe local link {target!r}")
                source_asset = root / requested_source
                try:
                    resolved_asset = source_asset.resolve()
                except OSError as error:
                    raise DocSproutError(f"{docs / page.path}: linked asset {document!r} cannot be resolved") from error
                if not resolved_asset.is_relative_to(root) or not resolved_asset.is_file():
                    raise DocSproutError(f"{docs / page.path}: linked asset {document!r} does not exist")
                asset_route = content_assets.get(requested_source)
                if asset_route is None:
                    asset_route = f"assets/content/{requested_source.removeprefix('docs/')}"
                    destination = output / asset_route
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(resolved_asset, destination)
                    content_assets[requested_source] = asset_route
                return _relative(current_route, asset_route) + (marker + fragment if marker else "")
            if marker and fragment not in anchors[requested]:
                raise DocSproutError(
                    f"{docs / page.path}: heading fragment #{fragment} does not exist in {requested}"
                )
            url = _relative(current_route, routes[requested])
            return url + (marker + fragment if marker else "")
        rendered = render_markdown(source, resolve)
        path = output / current_route
        path.parent.mkdir(parents=True, exist_ok=True)
        page_banner = banner if page.path == config.home_document and config.homepage.show_banner else None
        if versions:
            global_current_route = f"{release}/{current_route}"
            version_options = "".join(
                f'<option value="{html.escape(_relative(global_current_route, target), quote=True)}"{" selected" if item_release == release else ""}>{html.escape(item_release)}</option>'
                for item_release, target in versions
            )
        else:
            version_options = f'<option value="index.html">{html.escape(release)}</option>'
        path.write_text(_shell(body=rendered.html, headings=rendered.headings, page=page, config=config, current_route=current_route, version_options=version_options, banner=page_banner, logo=logo, release=release, custom_css=custom_css_route is not None), encoding="utf-8")
        entries.append({"title": rendered.title, "section": page.section, "url": current_route, "text": rendered.text})
    (output / "search-index.json").write_text(json.dumps({"schema_version": 1, "entries": entries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "release.json").write_text(json.dumps({"schema_version": 1, "release": release, "page_count": len(entries)}, indent=2) + "\n", encoding="utf-8")
    return BuildResult(
        len(entries), len({page.section for page in config.pages}), config.legacy,
        config.home_document, len(config.excluded_documents),
    )
