"""Unit and integration coverage for the derived, contrast-proven palette."""

from __future__ import annotations

import json
from pathlib import Path
import re
import tempfile
import unittest

from docsprout.assets import SITE_CSS
from docsprout.build import build_site
from docsprout.palette import (
    AA_TEXT,
    AA_UI,
    CLASSIC_DARK,
    CLASSIC_LIGHT,
    EINK_DARK,
    EINK_LIGHT,
    GLASS_DARK,
    GLASS_DARK_PROOF,
    GLASS_LIGHT,
    GLASS_LIGHT_PROOF,
    PAPER_DARK,
    PAPER_LIGHT,
    contrast_ratio,
    derive_palette,
    format_hex,
    parse_hex,
)

BACKGROUNDS = {
    ":root": CLASSIC_LIGHT,
    'html[data-visual-theme="paper"]': PAPER_LIGHT,
    'html[data-visual-theme="e-ink"]': EINK_LIGHT,
    'html[data-visual-theme="glassmorphic"]': GLASS_LIGHT_PROOF,
    'html[data-visual-theme="classic"][data-theme="dark"]': CLASSIC_DARK,
    'html[data-visual-theme="paper"][data-theme="dark"]': PAPER_DARK,
    'html[data-visual-theme="e-ink"][data-theme="dark"]': EINK_DARK,
    'html[data-visual-theme="glassmorphic"][data-theme="dark"]': GLASS_DARK_PROOF,
    'html[data-visual-theme="classic"]:not([data-theme])': CLASSIC_DARK,
    'html[data-visual-theme="paper"]:not([data-theme])': PAPER_DARK,
    'html[data-visual-theme="e-ink"]:not([data-theme])': EINK_DARK,
    'html[data-visual-theme="glassmorphic"]:not([data-theme])': GLASS_DARK_PROOF,
}


def _expand(value: str) -> str:
    if len(value) == 4:
        return "#" + "".join(character * 2 for character in value[1:])
    return value


def _token(selector: str, name: str) -> str:
    block = re.search(re.escape(selector) + r"\{([^}]*)\}", SITE_CSS)
    assert block is not None, selector
    value = re.search(rf"{name}:(#[0-9a-fA-F]{{3,6}})", block.group(1))
    assert value is not None, name
    return _expand(value.group(1).lower())


class PaletteMathTests(unittest.TestCase):
    def test_wcag_reference_contrast_and_formatting(self) -> None:
        self.assertAlmostEqual(21.0, contrast_ratio(parse_hex("#000000"), parse_hex("#ffffff")), places=1)
        self.assertAlmostEqual(1.0, contrast_ratio(parse_hex("#2563eb"), parse_hex("#2563eb")), places=5)
        self.assertEqual("#0f766e", format_hex(parse_hex("#0F766E")))

    def test_surface_constants_match_the_shipped_stylesheet(self) -> None:
        cases = (
            (":root", CLASSIC_LIGHT),
            ('html[data-theme="dark"]', CLASSIC_DARK),
            ('html[data-visual-theme="paper"]', PAPER_LIGHT),
            ('html[data-visual-theme="paper"][data-theme="dark"]', PAPER_DARK),
            ('html[data-visual-theme="e-ink"]', EINK_LIGHT),
            ('html[data-visual-theme="e-ink"][data-theme="dark"]', EINK_DARK),
            ('html[data-visual-theme="glassmorphic"]', GLASS_LIGHT),
            ('html[data-visual-theme="glassmorphic"][data-theme="dark"]', GLASS_DARK),
        )
        for selector, expected in cases:
            with self.subTest(selector=selector):
                actual = tuple(_token(selector, name) for name in ("--dk-bg", "--dk-surface", "--dk-raised"))
                self.assertEqual(expected, actual)


class PaletteDerivationTests(unittest.TestCase):
    def test_every_context_proves_text_and_ui_contrast(self) -> None:
        palette = derive_palette("#2563eb", "#0ea5e9")
        for entry in palette.entries:
            with self.subTest(selector=entry.selector):
                backgrounds = [parse_hex(value) for value in BACKGROUNDS[entry.selector]]
                interactive = parse_hex(entry.interactive)
                focus = parse_hex(entry.focus)
                for background in backgrounds:
                    self.assertGreaterEqual(contrast_ratio(interactive, background), AA_TEXT)
                    self.assertGreaterEqual(contrast_ratio(focus, background), AA_UI)
                self.assertGreaterEqual(contrast_ratio(parse_hex(entry.on_interactive), interactive), AA_TEXT)

    def test_a_passing_accent_keeps_the_exact_light_colour(self) -> None:
        palette = derive_palette("#2563eb", None)
        root = next(entry for entry in palette.entries if entry.selector == ":root")
        self.assertEqual("#2563eb", root.interactive)
        self.assertFalse(palette.light_adjusted)
        self.assertIsNone(palette.note)
        self.assertTrue(palette.secondary_derived)
        self.assertNotEqual("#2563eb", palette.accent_secondary)

    def test_an_explicit_secondary_is_preserved(self) -> None:
        palette = derive_palette("#2563eb", "#0891b2")
        self.assertFalse(palette.secondary_derived)
        self.assertEqual("#0891b2", palette.accent_secondary)

    def test_a_failing_accent_is_corrected_and_explained(self) -> None:
        palette = derive_palette("#ffff00", "#ffff00")
        root = next(entry for entry in palette.entries if entry.selector == ":root")
        self.assertNotEqual("#ffff00", root.interactive)
        self.assertGreaterEqual(contrast_ratio(parse_hex(root.interactive), parse_hex("#ffffff")), AA_TEXT)
        self.assertTrue(palette.light_adjusted)
        self.assertIn("#ffff00", palette.note)
        self.assertIn("WCAG AA", palette.note)
        for entry in palette.entries:
            backgrounds = [parse_hex(value) for value in BACKGROUNDS[entry.selector]]
            for background in backgrounds:
                self.assertGreaterEqual(contrast_ratio(parse_hex(entry.interactive), background), AA_TEXT)

    def test_stylesheet_overrides_every_theme_without_touching_documented_tokens(self) -> None:
        css = derive_palette("#0f766e", "#0891b2").stylesheet()
        for selector in (
            ":root{",
            'html[data-visual-theme="paper"]{',
            'html[data-visual-theme="glassmorphic"]{',
        ):
            self.assertIn(selector, css)
        # E-ink is ink-only: the stylesheet maps its links and focus to text.
        self.assertNotIn("e-ink", css)
        self.assertIn("@media(prefers-color-scheme:dark){", css)
        self.assertEqual(3, css.count(":not([data-theme])"))
        for documented in ("--dk-accent:", "--dk-accent-secondary:", "--dk-bg:"):
            self.assertNotIn(documented, css)


class PaletteIntegrationTests(unittest.TestCase):
    def test_built_pages_carry_corrected_values_and_a_result_note(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Home\n", encoding="utf-8")
            (docs / "docsprout.json").write_text(json.dumps({
                "schema_version": 1,
                "project": {"name": "Loud"},
                "theme": {"accent": "#ffff00"},
            }), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({"schema_version": 1, "navigation": [
                {"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]},
            ]}), encoding="utf-8")

            result = build_site(root=root, output=root / "site", release="dev")

            self.assertIsNotNone(result.palette_note)
            self.assertIn("WCAG AA", result.palette_note or "")
            home = (root / "site" / "index.html").read_text(encoding="utf-8")
            interactive = re.search(r"<style>:root\{--dk-interactive:(#[0-9a-f]{6});", home)
            self.assertIsNotNone(interactive)
            self.assertNotEqual("#ffff00", interactive.group(1))
            self.assertIn("--dk-on-interactive:", home)


THEME_BLOCKS = {
    "classic": (":root", 'html[data-theme="dark"]'),
    "paper": ('html[data-visual-theme="paper"]', 'html[data-visual-theme="paper"][data-theme="dark"]'),
    "e-ink": ('html[data-visual-theme="e-ink"]', 'html[data-visual-theme="e-ink"][data-theme="dark"]'),
    "glassmorphic": ('html[data-visual-theme="glassmorphic"]', 'html[data-visual-theme="glassmorphic"][data-theme="dark"]'),
}
CALLOUT_KINDS = ("note", "important", "tip", "warning")


def _callouts(selector: str) -> dict[str, str]:
    """Return the callout label colours declared in *selector*'s callout block."""
    block = re.search(re.escape(selector) + r"\{(--dk-callout-[^}]*)\}", SITE_CSS)
    assert block is not None, selector
    return {kind: _expand(re.search(rf"--dk-callout-{kind}:(#[0-9a-fA-F]{{3,6}})", block.group(1)).group(1)) for kind in CALLOUT_KINDS}


class ReadingContrastTests(unittest.TestCase):
    """Callout labels and the search placeholder meet WCAG AA text contrast."""

    def test_callout_labels_meet_text_contrast_on_every_callout_surface(self) -> None:
        light, dark = _callouts(":root"), _callouts('html[data-theme="dark"]')
        # System dark mode must use exactly the explicit dark values.
        self.assertEqual(dark, _callouts("html:not([data-theme])"))
        for theme, (light_selector, dark_selector) in THEME_BLOCKS.items():
            if theme == "e-ink":
                continue  # E-ink labels use --dk-text, covered by the body-text proof.
            for mode, selector, colours in (("light", light_selector, light), ("dark", dark_selector, dark)):
                surfaces = (_token(selector, "--dk-surface"), _token(selector, "--dk-bg"))
                for kind, colour in colours.items():
                    with self.subTest(theme=theme, mode=mode, kind=kind):
                        ratio = min(contrast_ratio(parse_hex(colour), parse_hex(surface)) for surface in surfaces)
                        self.assertGreaterEqual(ratio, AA_TEXT)

    def test_search_placeholder_meets_text_contrast_in_every_theme(self) -> None:
        self.assertIn(".topbar .search-control input::placeholder{color:var(--dk-muted);opacity:1}", SITE_CSS)
        for theme, selectors in THEME_BLOCKS.items():
            for selector in selectors:
                surfaces = [_token(selector, "--dk-surface")]
                if theme == "glassmorphic":
                    # Translucent glass controls: include the worst composites.
                    surfaces += list((GLASS_DARK_PROOF if "dark" in selector else GLASS_LIGHT_PROOF)[3:])
                muted = parse_hex(_token(selector, "--dk-muted"))
                with self.subTest(selector=selector):
                    self.assertGreaterEqual(min(contrast_ratio(muted, parse_hex(surface)) for surface in surfaces), AA_TEXT)


class InkOnlyEinkTests(unittest.TestCase):
    """E-ink renders in ink colours regardless of the configured accent."""

    def test_eink_maps_every_accent_token_to_ink(self) -> None:
        self.assertIn(
            'html[data-visual-theme="e-ink"] body{--dk-accent:var(--dk-text);--dk-accent-secondary:var(--dk-muted);'
            "--dk-interactive:var(--dk-text);--dk-focus-ring:var(--dk-text);--dk-on-interactive:var(--dk-bg)}",
            SITE_CSS,
        )
        self.assertIn('html[data-visual-theme="e-ink"] .syntax-highlight [class*="tok-"]{color:inherit}', SITE_CSS)

    def test_eink_callouts_differ_by_shape_not_colour(self) -> None:
        styles = {
            kind: re.search(r'html\[data-visual-theme="e-ink"\] \.admonition\.' + kind + r"\{([^}]*)\}", SITE_CSS).group(1)
            for kind in CALLOUT_KINDS
        }
        self.assertEqual(len(CALLOUT_KINDS), len(set(styles.values())))
        self.assertNotRegex("".join(styles.values()), r"#[0-9a-fA-F]{3,6}")


SYNTAX_KINDS = ("property", "keyword", "function", "string", "number", "constant", "comment")


def _syntax(selector: str) -> dict[str, str]:
    """Return the syntax token colours declared in *selector*'s syntax block."""
    block = re.search(re.escape(selector) + r"\{(--dk-syn-[^}]*)\}", SITE_CSS)
    assert block is not None, selector
    return {kind: _expand(re.search(rf"--dk-syn-{kind}:(#[0-9a-fA-F]{{3,6}})", block.group(1)).group(1)) for kind in SYNTAX_KINDS}


class ThemedCodeTests(unittest.TestCase):
    """Code blocks belong to their theme and stay readable."""

    def test_paper_syntax_meets_text_contrast_on_its_code_surface(self) -> None:
        light_selector = 'html[data-visual-theme="paper"]'
        dark_selector = 'html[data-visual-theme="paper"][data-theme="dark"]'
        self.assertEqual(_syntax(dark_selector), _syntax('html[data-visual-theme="paper"]:not([data-theme])'))
        for selector in (light_selector, dark_selector):
            code_bg = parse_hex(_token(selector, "--dk-code-bg"))
            colours = {"text": _token(selector, "--dk-code-text"), **_syntax(selector)}
            for kind, colour in colours.items():
                with self.subTest(selector=selector, kind=kind):
                    self.assertGreaterEqual(contrast_ratio(parse_hex(colour), code_bg), AA_TEXT)

    def test_window_dots_are_classic_only(self) -> None:
        self.assertIn('html:not([data-visual-theme="classic"]) .code-dots{display:none}', SITE_CSS)

    def test_reading_measure_is_set_in_characters(self) -> None:
        for snippet in (
            "--dk-reading-width:60ch;",
            'html[data-content-width="compact"]{--dk-content-width:40rem;--dk-reading-width:54ch;',
            'html[data-content-width="wide"]{--dk-content-width:54rem;--dk-reading-width:64ch;',
            'html[data-visual-theme="paper"]{--dk-reading-width:49ch}',
        ):
            self.assertIn(snippet, SITE_CSS)
