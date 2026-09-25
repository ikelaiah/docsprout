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
            'html[data-visual-theme="e-ink"]{',
            'html[data-visual-theme="glassmorphic"]{',
        ):
            self.assertIn(selector, css)
        self.assertIn("@media(prefers-color-scheme:dark){", css)
        self.assertEqual(4, css.count(":not([data-theme])"))
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
