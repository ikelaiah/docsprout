"""Versioned configuration loading and legacy-document discovery."""

from __future__ import annotations

import difflib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from .errors import DocSproutError
from .models import Homepage, Page, SiteConfig
from .palette import derive_palette

DEFAULT_ACCENT = "#2563eb"
DEFAULT_SECONDARY = "#0ea5e9"
HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")
THEME_PRESETS = {
    "blue": (DEFAULT_ACCENT, DEFAULT_SECONDARY),
    "teal": ("#0f766e", "#0891b2"),
    "ocean": ("#0369a1", "#0284c7"),
    "purple": ("#7c3aed", "#a855f7"),
}
THEME_STYLES = {"classic", "paper", "midnight"}
CONTENT_WIDTHS = {"compact", "comfortable", "wide"}
IDENTITY_LOGO_SUFFIXES = {".png", ".svg"}
HOMEPAGE_SECTION_DEFAULTS = {
    "capabilities": True,
    "banner": True,
    "introduction": True,
    "release_context": False,
}

CONFIG_FILENAME = "docsprout.json"
LEGACY_CONFIG_FILENAME = "dockit.json"
DOCSPROUT_FIELDS = ("schema_version", "project", "theme", "layout", "banner", "identity", "homepage")
PROJECT_FIELDS = ("name", "description", "repository_url", "site_url")
THEME_FIELDS = ("preset", "style", "accent", "accent_secondary", "custom_css")
LAYOUT_OPTION_FIELDS = ("content_width",)
BANNER_FIELDS = ("path", "alt")
IDENTITY_FIELDS = ("logo", "footer", "links")
HOMEPAGE_FIELDS = ("capabilities", "sections")
CAPABILITY_FIELDS = ("title", "description")
LINK_FIELDS = ("label", "url")
LAYOUT_FIELDS = ("schema_version", "home", "unlisted", "navigation")
HOME_FIELDS = ("path", "source")
SECTION_FIELDS = ("title", "pages")
PAGE_FIELDS = ("title", "path", "source")
MANIFEST_FIELDS = ("schema_version", "current", "versions")
VERSION_FIELDS = ("release", "source_ref")


def _reject_unknown_fields(
    value: object, allowed: tuple[str, ...], field_path: str, primary: Path,
) -> None:
    """Reject fields that never existed in a released schema-1 configuration.

    The allowed sets are the field families observed in the released v0.1.0
    through v0.17.0 tags, so valid historical configuration keeps loading
    while genuine typos fail with an actionable suggestion.
    """
    if not isinstance(value, dict):
        return
    for name in value:
        if name in allowed:
            continue
        suggestion = difflib.get_close_matches(name, allowed, n=1)
        hint = f" Did you mean '{field_path}.{suggestion[0]}'?" if suggestion else ""
        raise DocSproutError(f"{primary}: Unknown field '{field_path}.{name}'.{hint} Remove it or use a supported field.")


def _read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise DocSproutError(f"{path}: invalid JSON: {error}") from error
    if not isinstance(value, dict):
        raise DocSproutError(f"{path}: expected a JSON object")
    if value.get("schema_version") != 1:
        raise DocSproutError(f"{path}: only schema version 1 is supported; consult the migration guide before changing schema_version")
    return value


def safe_document_path(value: object, source_name: str) -> str:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise DocSproutError(f"{source_name}: path must be a non-empty relative path")
    path = Path(value)
    if any(part in {"", ".", ".."} for part in path.parts) or path.suffix.lower() != ".md":
        raise DocSproutError(f"{source_name}: invalid Markdown path {value!r}")
    return path.as_posix()


def page_source_path(root: Path, page: Page) -> Path:
    """Return the only allowed source location for a configured page."""
    candidate = root / "README.md" if page.source == "root" else root / "docs" / page.path
    resolved_root = root.resolve()
    try:
        resolved = candidate.resolve()
    except OSError as error:
        raise DocSproutError(f"Unsafe documentation source {candidate}") from error
    if not resolved.is_relative_to(resolved_root):
        raise DocSproutError(f"Unsafe documentation source outside the repository root: {candidate}")
    return resolved


def page_source_reference(page: Page) -> str:
    """Return the repository-relative path used for safe Markdown linking."""
    return "README.md" if page.source == "root" else f"docs/{page.path}"


def _home_page(paths: list[str]) -> str:
    priorities = ("index.md", "README.md", "readme.md", "start/index.md", "getting-started.md")
    for candidate in priorities:
        if candidate in paths:
            return candidate
    return paths[0]


def _title_from_path(path: str) -> str:
    return Path(path).stem.replace("-", " ").replace("_", " ").title()


def _homepage_config(data: dict, primary: Path) -> Homepage:
    raw_homepage = data.get("homepage", {})
    if not isinstance(raw_homepage, dict):
        raise DocSproutError(f"{primary}: field 'homepage' must be an object. Use a homepage object or remove the field.")
    _reject_unknown_fields(raw_homepage, HOMEPAGE_FIELDS, "homepage", primary)
    if "capabilities" not in raw_homepage:
        capabilities = None
    else:
        raw_capabilities = raw_homepage["capabilities"]
        if not isinstance(raw_capabilities, list):
            raise DocSproutError(f"{primary}: field 'homepage.capabilities' must be a list. Use a list of title and description objects.")
        cards: list[tuple[str, str]] = []
        for index, card in enumerate(raw_capabilities):
            if not isinstance(card, dict):
                raise DocSproutError(f"{primary}: homepage.capabilities[{index}] must be an object. Use title and description fields.")
            _reject_unknown_fields(card, CAPABILITY_FIELDS, f"homepage.capabilities[{index}]", primary)
            values: list[str] = []
            for field in ("title", "description"):
                value = card.get(field)
                if not isinstance(value, str) or not value.strip():
                    raise DocSproutError(f"{primary}: homepage.capabilities[{index}].{field} must be a non-empty string. Use a non-empty string.")
                values.append(value.strip())
            cards.append((values[0], values[1]))
        capabilities = tuple(cards)
    raw_sections = raw_homepage.get("sections", {})
    if not isinstance(raw_sections, dict):
        raise DocSproutError(f"{primary}: field 'homepage.sections' must be an object. Use section names with true or false values.")
    for name in raw_sections:
        if name not in HOMEPAGE_SECTION_DEFAULTS:
            choices = ", ".join(HOMEPAGE_SECTION_DEFAULTS)
            raise DocSproutError(f"{primary}: homepage.sections.{name} is not supported. Use one of {choices}.")
    sections: dict[str, bool] = {}
    for name, default in HOMEPAGE_SECTION_DEFAULTS.items():
        value = raw_sections.get(name, default)
        if not isinstance(value, bool):
            raise DocSproutError(f"{primary}: homepage.sections.{name} must be a boolean. Use true or false.")
        sections[name] = value
    return Homepage(
        capabilities=capabilities,
        show_capabilities=sections["capabilities"],
        show_banner=sections["banner"],
        show_introduction=sections["introduction"],
        show_release_context=sections["release_context"],
    )


def _identity_logo_path(root: Path, identity: dict, primary: Path) -> str | None:
    value = identity.get("logo")
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise DocSproutError(f"{primary}: field 'identity.logo' must be a non-empty repository-local SVG or PNG path")
    path = Path(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise DocSproutError(f"{primary}: identity.logo path is unsafe")
    if path.suffix.lower() not in IDENTITY_LOGO_SUFFIXES:
        raise DocSproutError(f"{primary}: identity.logo must reference an SVG or PNG file")
    candidate = root / path
    try:
        resolved = candidate.resolve()
    except OSError as error:
        raise DocSproutError(f"{primary}: identity.logo asset {value!r} cannot be resolved") from error
    if not resolved.is_relative_to(root.resolve()):
        raise DocSproutError(f"{primary}: identity.logo path is unsafe")
    if not resolved.is_file():
        raise DocSproutError(f"{primary}: identity.logo asset {value!r} does not exist")
    return path.as_posix()


def _custom_css_path(root: Path, theme: dict, primary: Path) -> str | None:
    value = theme.get("custom_css")
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise DocSproutError(f"{primary}: field 'theme.custom_css' must be a non-empty repository-local CSS path")
    path = Path(value)
    drive_absolute = re.match(r"^[A-Za-z]:[\\/]", value) is not None
    if path.is_absolute() or drive_absolute or any(part in {"", ".", ".."} for part in path.parts):
        raise DocSproutError(f"{primary}: theme.custom_css path is unsafe; use a repository-local relative path")
    if path.suffix.lower() != ".css":
        raise DocSproutError(f"{primary}: theme.custom_css must reference a .css file")
    candidate = root / path
    try:
        resolved = candidate.resolve()
    except OSError as error:
        raise DocSproutError(f"{primary}: theme.custom_css asset {value!r} cannot be resolved") from error
    if not resolved.is_relative_to(root.resolve()):
        raise DocSproutError(
            f"{primary}: theme.custom_css asset {value!r} resolves outside the repository root; keep the stylesheet inside the repository"
        )
    if not resolved.is_file():
        raise DocSproutError(f"{primary}: theme.custom_css asset {value!r} does not exist")
    return path.as_posix()


def _legacy_config(docs: Path) -> SiteConfig:
    paths = sorted(path.relative_to(docs).as_posix() for path in docs.rglob("*.md"))
    if not paths:
        raise DocSproutError(f"{docs}: no Markdown documents found")
    home = _home_page(paths)
    pages = tuple(Page(path, _title_from_path(path)) for path in paths)
    return SiteConfig(
        name="Documentation", description="Historical documentation", repository_url=None,
        site_url=None, accent=DEFAULT_ACCENT, accent_secondary=DEFAULT_SECONDARY, theme_style="classic",
        content_width="comfortable",
        banner=None, banner_alt=None, logo=None, footer=None, project_links=(), pages=pages,
        legacy=True, home_document=home,
        homepage=Homepage(None, True, True, True, False),
        excluded_documents=(),
        palette=derive_palette(DEFAULT_ACCENT, DEFAULT_SECONDARY),
    )


def resolve_config_path(docs: Path) -> Path | None:
    """Return the single supported configuration file below *docs*.

    ``docsprout.json`` is canonical. A pre-rebrand ``dockit.json`` keeps
    loading for the 1.x compatibility window. When both exist the project is
    ambiguous, so the caller receives an actionable error instead of a silent
    choice.
    """
    primary = docs / CONFIG_FILENAME
    legacy = docs / LEGACY_CONFIG_FILENAME
    if primary.is_file() and legacy.is_file():
        raise DocSproutError(
            f"{docs}: both {CONFIG_FILENAME} and {LEGACY_CONFIG_FILENAME} exist. "
            f"DocSprout cannot choose one silently: keep {CONFIG_FILENAME} (recommended) and delete "
            f"{LEGACY_CONFIG_FILENAME}, or remove {CONFIG_FILENAME} to keep the legacy name."
        )
    if primary.is_file():
        return primary
    if legacy.is_file():
        return legacy
    return None


def load_config(root: Path, *, require_listed_documents: bool = True) -> SiteConfig:
    """Load configuration, optionally applying current navigation completeness rules."""
    docs = root / "docs"
    primary = resolve_config_path(docs)
    layout_path = docs / "layout.json"
    if primary is None and not layout_path.exists():
        return _legacy_config(docs)
    if primary is None:
        raise DocSproutError(f"{docs / CONFIG_FILENAME}: required when modern documentation configuration exists")
    data = _read_json(primary)
    _reject_unknown_fields(data, DOCSPROUT_FIELDS, primary.stem, primary)
    homepage = _homepage_config(data, primary)
    project = data.get("project")
    if not isinstance(project, dict) or not isinstance(project.get("name"), str) or not project["name"].strip():
        raise DocSproutError(f"{primary}: field 'project.name' must be a non-empty string")
    _reject_unknown_fields(project, PROJECT_FIELDS, "project", primary)
    for field in ("description", "repository_url", "site_url"):
        value = project.get(field)
        if value is not None and not isinstance(value, str):
            raise DocSproutError(f"{primary}: field 'project.{field}' must be a string when provided")
    theme = data.get("theme", {})
    if not isinstance(theme, dict):
        raise DocSproutError(f"{primary}: field 'theme' must be an object")
    _reject_unknown_fields(theme, THEME_FIELDS, "theme", primary)
    custom_css = _custom_css_path(root, theme, primary)
    preset = theme.get("preset", "blue")
    if not isinstance(preset, str) or preset not in THEME_PRESETS:
        choices = ", ".join(THEME_PRESETS)
        raise DocSproutError(f"{primary}: field 'theme.preset' must be one of {choices}. Choose a supported preset or remove the field.")
    preset_accent, preset_secondary = THEME_PRESETS[preset]
    theme_style = theme.get("style", "classic")
    if not isinstance(theme_style, str) or theme_style not in THEME_STYLES:
        raise DocSproutError(f"{primary}: field 'theme.style' must be one of {', '.join(sorted(THEME_STYLES))}. Choose a supported visual theme or remove the field.")
    accent = theme.get("accent", preset_accent)
    if not isinstance(accent, str) or not HEX_COLOR.fullmatch(accent):
        raise DocSproutError(
            f"{primary}: field 'theme.accent' must be a #RRGGBB colour. "
            "Use a #RRGGBB colour such as #0f766e."
        )
    requested_secondary = theme.get("accent_secondary")
    if requested_secondary is not None and (not isinstance(requested_secondary, str) or not HEX_COLOR.fullmatch(requested_secondary)):
        raise DocSproutError(
            f"{primary}: field 'theme.accent_secondary' must be a #RRGGBB colour. "
            "Use a #RRGGBB colour such as #0891b2."
        )
    # One configured accent is a complete theme: when a project sets an accent
    # without a secondary, DocSprout derives an analogous secondary from it.
    # Curated presets keep their documented colour pair.
    secondary_source = requested_secondary
    if secondary_source is None and "accent" not in theme:
        secondary_source = preset_secondary
    palette = derive_palette(accent, secondary_source)
    secondary = palette.accent_secondary
    layout_options = data.get("layout", {})
    if not isinstance(layout_options, dict):
        raise DocSproutError(f"{primary}: field 'layout' must be an object. Use a layout object or remove the field.")
    _reject_unknown_fields(layout_options, LAYOUT_OPTION_FIELDS, "layout", primary)
    content_width = layout_options.get("content_width", "comfortable")
    if not isinstance(content_width, str) or content_width not in CONTENT_WIDTHS:
        raise DocSproutError(
            f"{primary}: field 'layout.content_width' must be one of compact, comfortable, wide. "
            "Choose a supported content width or remove the field."
        )
    if not layout_path.exists():
        raise DocSproutError(f"{layout_path}: required for modern documentation")
    layout = _read_json(layout_path)
    _reject_unknown_fields(layout, LAYOUT_FIELDS, "layout", layout_path)
    unlisted = layout.get("unlisted", "error")
    if unlisted not in {"error", "exclude"}:
        raise DocSproutError(f"{layout_path}: field 'unlisted' must be 'error' or 'exclude'")
    navigation = layout.get("navigation")
    if not isinstance(navigation, list) or not navigation:
        raise DocSproutError(f"{layout_path}: field 'navigation' must be a non-empty list")
    pages: list[Page] = []
    for section in navigation:
        if not isinstance(section, dict) or not isinstance(section.get("title"), str) or not section["title"].strip():
            raise DocSproutError(f"{layout_path}: each navigation section needs a non-empty title")
        _reject_unknown_fields(section, SECTION_FIELDS, f"navigation.{section.get('title')}", layout_path)
        entries = section.get("pages")
        if not isinstance(entries, list) or not entries:
            raise DocSproutError(
                f"{layout_path}: navigation section {section['title']!r} needs pages. "
                "Add at least one page entry or remove the section."
            )
        for entry in entries:
            if not isinstance(entry, dict) or not isinstance(entry.get("title"), str) or not entry["title"].strip():
                raise DocSproutError(f"{layout_path}: navigation page needs a non-empty title")
            _reject_unknown_fields(entry, PAGE_FIELDS, f"navigation.{section['title']}.pages", layout_path)
            path = safe_document_path(entry.get("path"), f"{layout_path}: navigation page")
            source = entry.get("source", "docs")
            if source not in {"docs", "root"}:
                raise DocSproutError(f"{layout_path}: navigation page source must be 'docs' or 'root'")
            if source == "root" and path != "README.md":
                raise DocSproutError(f"{layout_path}: repository-root source only supports README.md")
            page = Page(path, entry["title"], section["title"], source)
            if not page_source_path(root, page).is_file():
                location = "README.md" if source == "root" else f"docs/{path}"
                raise DocSproutError(
                    f"{layout_path}: navigation page {path!r} does not exist. "
                    f"Create {location} or correct its path."
                )
            if any(page.path == path for page in pages):
                raise DocSproutError(f"{layout_path}: navigation page {path!r} appears more than once")
            pages.append(page)
    listed_paths = {page.path for page in pages}
    unlisted_paths = sorted(path.relative_to(docs).as_posix() for path in docs.rglob("*.md") if path.is_file() and path.relative_to(docs).as_posix() not in listed_paths)
    if require_listed_documents and unlisted == "error" and unlisted_paths:
        raise DocSproutError(f"{layout_path}: unlisted Markdown document {unlisted_paths[0]!r}. Add it to navigation or remove it.")
    excluded_documents = tuple(unlisted_paths) if unlisted == "exclude" else ()
    raw_home = layout.get("home")
    if raw_home is None:
        home = next((page.path for page in pages if page.source == "root"), None)
        if home is None:
            home = "index.md" if any(page.path == "index.md" for page in pages) else pages[0].path
    else:
        if not isinstance(raw_home, dict):
            raise DocSproutError(f"{layout_path}: field 'home' must be an object with a listed page path")
        _reject_unknown_fields(raw_home, HOME_FIELDS, "home", layout_path)
        path = safe_document_path(raw_home.get("path"), f"{layout_path}: home")
        source = raw_home.get("source", "docs")
        if source not in {"docs", "root"}:
            raise DocSproutError(f"{layout_path}: home.source must be 'docs' or 'root'")
        if source == "root" and path != "README.md":
            raise DocSproutError(f"{layout_path}: repository-root source only supports README.md")
        if source == "docs" and path == "README.md":
            raise DocSproutError(f"{layout_path}: home README.md requires source 'root'")
        if not any(page.path == path and page.source == source for page in pages):
            raise DocSproutError(f"{layout_path}: home.path {path!r} must name a listed navigation page with the same source")
        home = path
    banner = data.get("banner")
    if banner is not None and (not isinstance(banner, dict) or not isinstance(banner.get("path"), str) or not isinstance(banner.get("alt"), str)):
        raise DocSproutError(f"{primary}: field 'banner' needs string path and alt fields")
    _reject_unknown_fields(banner, BANNER_FIELDS, "banner", primary)
    banner_path = banner["path"] if banner else None
    if banner_path and (Path(banner_path).is_absolute() or ".." in Path(banner_path).parts):
        raise DocSproutError(f"{primary}: banner path is unsafe")
    if banner_path and not (root / banner_path).is_file():
        raise DocSproutError(f"{primary}: banner asset {banner_path!r} does not exist")
    if banner_path and not (root / banner_path).resolve().is_relative_to(root.resolve()):
        raise DocSproutError(f"{primary}: banner asset {banner_path!r} is outside the repository root")
    identity = data.get("identity", {})
    if not isinstance(identity, dict):
        raise DocSproutError(f"{primary}: field 'identity' must be an object")
    _reject_unknown_fields(identity, IDENTITY_FIELDS, "identity", primary)
    logo = _identity_logo_path(root, identity, primary)
    footer = identity.get("footer")
    if footer is not None and (not isinstance(footer, str) or not footer.strip()):
        raise DocSproutError(f"{primary}: field 'identity.footer' must be a non-empty string when provided")
    raw_links = identity.get("links", [])
    if not isinstance(raw_links, list):
        raise DocSproutError(f"{primary}: field 'identity.links' must be a list")
    project_links: list[tuple[str, str]] = []
    for index, link in enumerate(raw_links):
        if not isinstance(link, dict) or not isinstance(link.get("label"), str) or not link["label"].strip() or not isinstance(link.get("url"), str):
            raise DocSproutError(f"{primary}: identity.links[{index}] needs non-empty string label and URL fields")
        _reject_unknown_fields(link if isinstance(link, dict) else {}, LINK_FIELDS, f"identity.links[{index}]", primary)
        parsed = urlsplit(link["url"])
        if parsed.scheme not in {"https", "http"} or not parsed.netloc:
            raise DocSproutError(f"{primary}: identity.links[{index}].url must be an absolute http(s) URL")
        project_links.append((link["label"].strip(), link["url"]))
    return SiteConfig(
        name=project["name"].strip(), description=str(project.get("description", "")),
        repository_url=project.get("repository_url"), site_url=project.get("site_url"),
        accent=accent, accent_secondary=secondary, theme_style=theme_style, content_width=content_width,
        banner=banner_path,
        banner_alt=banner.get("alt") if banner else None, logo=logo, footer=footer.strip() if footer else None,
        project_links=tuple(project_links), pages=tuple(pages),
        legacy=False, home_document=home, homepage=homepage,
        custom_css=custom_css, excluded_documents=excluded_documents,
        config_filename=primary.name, palette=palette,
    )
