"""Qualification: accessibility fundamentals of generated sites.

Objective, structural assertions over the maintained visual fixture and
DocSprout's own built documentation: keyboard-operable native controls, visible
focus, accessible names, the search keyboard contract, heading structure,
callout labels, reduced-motion, scroller containment and the shared semantic
theme-token contract for Classic/Paper/E-ink/Glassmorphic in Light/Dark/System.

Visual/interactive behaviour that cannot be asserted structurally is covered
by the manual matrix documented in docs/qualification.md.
"""

from __future__ import annotations

import re
from pathlib import Path
import tempfile
import unittest

from docsprout.assets import SITE_CSS, SITE_JS
from docsprout.build import build_site

REPO_ROOT = Path(__file__).resolve().parents[1]
NATIVE_INTERACTIVE = {"a", "button", "input", "select", "summary", "details"}
TAG = re.compile(r"<(/)?([a-z][a-z0-9-]*)\b[^>]*>", re.IGNORECASE)
OPENING_TAG = re.compile(r"<([a-z][a-z0-9-]*)\b[^>]*>", re.IGNORECASE)
HEADING = re.compile(r"<h([1-6])\b[^>]*>(.*?)</h\1>", re.DOTALL)
LINK = re.compile(r'<a\b([^>]*)\bhref="([^"]*)"([^>]*)>(.*?)</a>', re.DOTALL)
IMAGE = re.compile(r"<img\b[^>]*>")
ATTRIBUTE = re.compile(r'([a-z-]+)="([^"]*)"', re.IGNORECASE)
VOID_TAG = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
INTERACTIVE_ATTRIBUTE = re.compile(r"\b(onclick|onkeydown|onkeyup|onkeypress|tabindex)\s*=", re.IGNORECASE)
PUBLIC_TOKENS = (
    "--dk-accent", "--dk-accent-secondary", "--dk-bg", "--dk-surface", "--dk-text", "--dk-muted",
    "--dk-border", "--dk-code-bg", "--dk-code-text", "--dk-raised", "--dk-focus-ring",
    "--dk-interactive", "--dk-content-width", "--dk-reading-width", "--dk-shell-width",
)
LEGACY_TOKENS = ("--bg", "--surface", "--text", "--muted", "--border", "--code", "--raised", "--focus-ring", "--interactive")
CHROMATIC_TOKENS = (
    "--dk-bg", "--dk-surface", "--dk-text", "--dk-muted", "--dk-border",
    "--dk-code-bg", "--dk-raised", "--dk-focus-ring", "--dk-interactive",
)


def _theme_tokens(css: str, selector: str) -> set[str]:
    match = re.search(re.escape(selector) + r"\{([^}]*)\}", css)
    if match is None:
        return set()
    return {token for token in PUBLIC_TOKENS if token in match.group(1)}


def _open_tags(html: str) -> list[str]:
    return [match.group(1).lower() for match in OPENING_TAG.finditer(html)]


def _slug(value: str) -> bool:
    return bool(value) and not re.search(r"\s", value)


class _Site:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.files: dict[str, str] = {}
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "site"
            build_site(root=root, output=output, release="accessibility")
            for path in output.rglob("*.html"):
                self.files[path.relative_to(output).as_posix()] = path.read_text(encoding="utf-8")
            self.css = (output / "assets" / "site.css").read_text(encoding="utf-8")
            self.js = (output / "assets" / "site.js").read_text(encoding="utf-8")


class AccessibilityQualificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture = REPO_ROOT / "examples" / "visual-fixtures"
        cls.fixture = _Site(fixture)
        cls.docsprout = _Site(REPO_ROOT)

    def test_controls_are_native_keyboard_operable_elements(self) -> None:
        for name, site in (("fixture", self.fixture), ("DocSprout", self.docsprout)):
            with self.subTest(site=name):
                for route, page in site.files.items():
                    self.assertNotRegex(page, INTERACTIVE_ATTRIBUTE, route)
                    interactive = {tag for tag in _open_tags(page) if tag in NATIVE_INTERACTIVE}
                    self.assertTrue({"input", "select", "summary", "a"} <= interactive, route)

    def test_focus_indicators_are_visible_in_every_theme(self) -> None:
        css = self.fixture.css
        self.assertIn(
            "button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid var(--dk-focus-ring);outline-offset:3px}",
            css,
        )
        for theme in ("classic", "paper", "e-ink", "glassmorphic"):
            self.assertIn(f'html[data-visual-theme="{theme}"]', css)
        self.assertIn("@media(forced-colors:active)", css)
        self.assertIn("outline-color:Highlight", css)

    def test_search_is_keyboard_operable_and_announced(self) -> None:
        page = self.fixture.files["index.html"]
        self.assertIn('<input id="search" type="search"', page)
        self.assertIn('aria-label="Search documentation, commands, and versions"', page)
        self.assertIn('aria-controls="search-results"', page)
        self.assertIn('aria-describedby="search-help"', page)
        self.assertIn('aria-expanded="false"', page)
        self.assertIn('id="search-help" class="visually-hidden"', page)
        self.assertIn('role="region" aria-label="Search results" aria-live="polite" hidden', page)
        for contract in ("ArrowDown", "ArrowUp", "Home", "End", "Escape", "event.key==='/'", "preventDefault()", ".focus()"):
            self.assertIn(contract, self.fixture.js, contract)
        self.assertIn("showSearch()", self.fixture.js)
        self.assertIn("results.hidden=false", self.fixture.js)

    def test_mobile_navigation_is_a_keyboard_operable_details_element(self) -> None:
        for name, site in (("fixture", self.fixture), ("DocSprout", self.docsprout)):
            with self.subTest(site=name):
                for route, page in site.files.items():
                    self.assertIn('<details class="mobile-nav">', page, route)
                    self.assertIn("<summary>Browse documentation</summary>", page, route)
                    self.assertIn('</details>', page, route)
                    self.assertIn('summary{cursor:pointer}', site.css)

    def test_theme_and_mode_controls_have_accessible_names_and_full_options(self) -> None:
        page = self.fixture.files["index.html"]
        self.assertIn('aria-label="Site controls"', page)
        self.assertIn('aria-label="Documentation version"', page)
        self.assertIn('aria-label="Colour theme"', page)
        self.assertIn('aria-label="Documentation visual theme"', page)
        self.assertIn("<option value=\"system\">System</option>", page)
        self.assertIn("<option value=\"light\">Light</option>", page)
        self.assertIn("<option value=\"dark\">Dark</option>", page)
        for theme in ("classic", "paper", "e-ink", "glassmorphic"):
            self.assertIn(f'<option value="{theme}">{theme.capitalize()}</option>', page)
        self.assertIn('data-visual-theme="classic"', page)
        self.assertIn("prefers-color-scheme:dark", self.fixture.css)

    def test_previous_next_navigation_remains_understandable(self) -> None:
        page = self.fixture.files["long-form.html"]
        self.assertIn('<nav class="page-navigation" aria-label="Page navigation">', page)
        self.assertIn("<small>Previous</small>", page)
        self.assertIn('class="page-previous"', page)
        self.assertNotIn("page-next", page)
        first = self.fixture.files["index.html"]
        self.assertIn("<small>Next</small>", first)
        self.assertIn('class="page-next"', first)
        for name, site in (("fixture", self.fixture), ("DocSprout", self.docsprout)):
            with self.subTest(site=name):
                for route, page in site.files.items():
                    self.assertRegex(page, r'<nav class="page-navigation" aria-label="Page navigation">', route)
                    for link in LINK.finditer(page):
                        self.assertNotIn("javascript:", link.group(2), route)

    def test_headings_keep_single_h1_structure_and_usable_toc_links(self) -> None:
        for name, site in (("fixture", self.fixture), ("DocSprout", self.docsprout)):
            with self.subTest(site=name):
                for route, page in site.files.items():
                    main = page[page.index("<main"):page.index("</main>")]
                    levels = [(int(level), text) for level, text in HEADING.findall(main)]
                    self.assertEqual(1, sum(1 for level, _ in levels if level == 1), route)
                    previous = 0
                    for level, _text in levels:
                        self.assertLessEqual(level, previous + 1, f"{route}: heading jump to h{level}")
                        previous = level
                    identifiers = [match.group(1) for match in re.finditer(r'<h[1-6][^>]*id="([^"]+)"', main)]
                    self.assertTrue(identifiers, route)
                    for identifier in identifiers:
                        self.assertTrue(_slug(identifier), f"{route}: unsluggified heading id {identifier!r}")

    def test_links_are_usable_and_safe(self) -> None:
        for name, site in (("fixture", self.fixture), ("DocSprout", self.docsprout)):
            with self.subTest(site=name):
                for route, page in site.files.items():
                    for _before, href, _after, label in LINK.findall(page):
                        self.assertNotIn("javascript:", href, route)
                        if href.startswith("http"):
                            self.assertRegex(href, r"^https?://[^/\s]", route)
                        else:
                            self.assertIn(href, page, f"{route}: href {href!r} without anchor context")
                    for image in IMAGE.findall(page):
                        attributes = dict(ATTRIBUTE.findall(image))
                        self.assertIn("alt", attributes, f"{route}: img without alt")
                        self.assertTrue(attributes["src"], f"{route}: img without src")

    def test_callouts_carry_a_text_label_not_only_colour(self) -> None:
        for name, site in (("fixture", self.fixture), ("DocSprout", self.docsprout)):
            with self.subTest(site=name):
                for route, page in site.files.items():
                    for admonition in re.findall(r'<aside class="admonition [a-z]+">(.*?)</aside>', page):
                        self.assertRegex(admonition, r"<strong>", f"{route}: callout without text label")
                    self.assertIn(".admonition.note", site.css)
                    self.assertIn(".admonition.warning", site.css)
                    self.assertIn(".admonition.tip", site.css)
                    self.assertIn(".admonition.important", site.css)

    def test_reduced_motion_and_scroller_containment_are_preserved(self) -> None:
        css = self.fixture.css
        self.assertIn(
            "@media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;transition-duration:.01ms!important;animation-duration:.01ms!important;animation-iteration-count:1!important}}",
            css,
        )
        self.assertRegex(css, r"\.prose pre\{[^}]*overflow:auto")
        self.assertRegex(css, r"\.table-scroll\{[^}]*overflow:auto")
        self.assertRegex(css, r"\.sidebar\{[^}]*overflow:auto")
        self.assertIn("min-width:max-content", css)
        self.assertIn("overflow-wrap:anywhere", css)

    def test_light_dark_system_modes_are_coherent_across_themes(self) -> None:
        css = self.fixture.css
        base = _theme_tokens(css, ":root")
        self.assertEqual(set(PUBLIC_TOKENS), base)
        for selector in (
            'html[data-theme="dark"]',
            'html[data-visual-theme="paper"][data-theme="dark"]',
            'html[data-visual-theme="e-ink"]',
            'html[data-visual-theme="e-ink"][data-theme="dark"]',
            'html[data-visual-theme="glassmorphic"]',
            'html[data-visual-theme="glassmorphic"][data-theme="dark"]',
        ):
            coverage = _theme_tokens(css, selector) | base
            self.assertEqual(set(PUBLIC_TOKENS), coverage, selector)
        paper_light = _theme_tokens(css, 'html[data-visual-theme="paper"]') | base
        self.assertEqual(set(PUBLIC_TOKENS), paper_light, "paper light")
        paper_system_dark = re.search(
            r'@media\(prefers-color-scheme:dark\)\{html\[data-visual-theme="paper"\]:not\(\[data-theme\]\)\{([^}]*)\}\}',
            css,
        )
        self.assertIsNotNone(paper_system_dark)
        paper_system_tokens = {token for token in PUBLIC_TOKENS if token in paper_system_dark.group(1)} | base
        self.assertEqual(set(PUBLIC_TOKENS), paper_system_tokens, "paper system dark")
        self.assertIn('html[data-theme="light"]{color-scheme:light}', css)
        self.assertIn('html[data-theme="dark"]{color-scheme:dark', css)
        for theme in ("classic", "paper", "e-ink", "glassmorphic"):
            self.assertIn(f'html[data-visual-theme="{theme}"]', css, theme)
        self.assertIn("@supports ((backdrop-filter:blur(2px)) or (-webkit-backdrop-filter:blur(2px)))", css)
        self.assertIn("--dk-shadow:none", css)

    def test_the_classic_system_dark_variant_defines_the_full_token_contract(self) -> None:
        system_blocks = re.findall(
            r'@media\(prefers-color-scheme:dark\)\{html\[data-visual-theme="classic"\]:not\(\[data-theme\]\)\{([^}]*)\}\}',
            self.fixture.css,
        )
        self.assertEqual(1, len(system_blocks))
        merged = "".join(system_blocks)
        for token in CHROMATIC_TOKENS:
            self.assertIn(token, merged)

    def test_the_public_dk_token_family_is_namespaced_complete_and_used(self) -> None:
        css = self.fixture.css
        for legacy in LEGACY_TOKENS:
            self.assertNotIn(f"{legacy}:", css, f"legacy token {legacy} survived the pre-1.0 rename")
            self.assertNotIn(f"var({legacy})", css, f"legacy token {legacy} is still referenced")
        root = _theme_tokens(css, ":root")
        self.assertEqual(set(PUBLIC_TOKENS), root, ":root must define every documented public token")
        for token in PUBLIC_TOKENS:
            self.assertIn(f"var({token})", css, f"public token {token} is defined but never used")

    def test_every_generated_page_has_document_structure(self) -> None:
        for name, site in (("fixture", self.fixture), ("DocSprout", self.docsprout)):
            with self.subTest(site=name):
                for route, page in site.files.items():
                    self.assertTrue(page.startswith("<!doctype html>"), route)
                    self.assertIn('<html lang="en"', page, route)
                    self.assertIn('<meta name="viewport" content="width=device-width,initial-scale=1">', page, route)
                    self.assertRegex(page, r"<title>[^<]+</title>", route)
                    self.assertIn('<main class="prose" id="content"', page, route)
                    self.assertIn('<nav class="sidebar" aria-label="Documentation navigation">', page, route)
                    self.assertIn('class="visually-hidden"', page, route)

    def test_accessible_copy_controls_use_button_with_a_label(self) -> None:
        for cross_check in ("button.type='button'", "setCopyLabel('Copy code')", "aria-label", "Copy unavailable"):
            self.assertIn(cross_check, SITE_JS)
        self.assertIn(".copy-code", SITE_CSS)

    def test_docsprout_own_site_builds_the_shared_accessibility_contract(self) -> None:
        self.assertTrue(self.docsprout.files)
        home = self.docsprout.files["index.html"]
        for shared in (
            'aria-label="Search documentation, commands, and versions"',
            '<details class="mobile-nav">',
            '<nav class="page-navigation" aria-label="Page navigation">',
            'aria-label="Colour theme"',
            'aria-label="Documentation visual theme"',
            '<nav class="sidebar" aria-label="Documentation navigation">',
        ):
            self.assertIn(shared, home)
        self.assertEqual(self.fixture.css, self.docsprout.css)