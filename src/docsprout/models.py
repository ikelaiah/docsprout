"""Small, explicit data models used by the documentation pipeline."""

from dataclasses import dataclass

from .palette import Palette


@dataclass(frozen=True)
class Page:
    path: str
    title: str
    section: str = "Documentation"
    source: str = "docs"
    subsection: str | None = None


@dataclass(frozen=True)
class Homepage:
    capabilities: tuple[tuple[str, str], ...] | None
    show_capabilities: bool
    show_banner: bool
    show_introduction: bool
    show_release_context: bool


@dataclass(frozen=True)
class SiteConfig:
    name: str
    description: str
    repository_url: str | None
    site_url: str | None
    accent: str
    accent_secondary: str
    theme_style: str
    content_width: str
    banner: str | None
    banner_alt: str | None
    logo: str | None
    footer: str | None
    project_links: tuple[tuple[str, str], ...]
    pages: tuple[Page, ...]
    legacy: bool
    home_document: str
    homepage: Homepage
    custom_css: str | None = None
    excluded_documents: tuple[str, ...] = ()
    config_filename: str | None = None
    palette: Palette | None = None
    expanded_sections: tuple[str, ...] = ()
    expanded_groups: tuple[tuple[str, str], ...] = ()
