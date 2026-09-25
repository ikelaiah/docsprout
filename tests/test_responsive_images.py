import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

from docsprout.assets import SITE_CSS
from docsprout.build import build_site
from docsprout.versions import build_all


def _declarations(css: str, selector: str) -> dict[str, str]:
    """Collect the final declaration for each occurrence of a CSS selector."""
    declarations: dict[str, str] = {}
    blocks = re.findall(rf"{re.escape(selector)}\{{([^}}]*)\}}", css)
    if not blocks:
        raise AssertionError(f"CSS selector {selector!r} is missing")
    for block in blocks:
        for declaration in block.split(";"):
            if ":" not in declaration:
                continue
            property_name, value = declaration.split(":", 1)
            declarations[property_name] = value
    return declarations


class ResponsiveProseImageTests(unittest.TestCase):
    def _project(
        self,
        root: Path,
        *,
        content_width: str = "comfortable",
        theme_style: str = "classic",
        custom_css: str | None = None,
        banner: bool = False,
    ) -> None:
        docs = root / "docs"
        assets = docs / "assets"
        assets.mkdir(parents=True)
        (docs / "index.md").write_text(
            "# Image fixture\n\n"
            "![Oversized illustration](assets/oversized.svg)\n\n"
            "![Small badge](assets/badge.svg)\n",
            encoding="utf-8",
        )
        (assets / "oversized.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="1983" height="793" '
            'viewBox="0 0 1983 793"><rect width="1983" height="793"/></svg>',
            encoding="utf-8",
        )
        (assets / "badge.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" '
            'viewBox="0 0 32 32"><circle cx="16" cy="16" r="15"/></svg>',
            encoding="utf-8",
        )
        config: dict = {
            "schema_version": 1,
            "project": {"name": "Responsive images"},
            "theme": {"style": theme_style},
            "layout": {"content_width": content_width},
        }
        if custom_css is not None:
            (assets / "custom.css").write_text(custom_css, encoding="utf-8")
            config["theme"]["custom_css"] = "docs/assets/custom.css"
        if banner:
            (assets / "banner.svg").write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" '
                'viewBox="0 0 1200 300"><rect width="1200" height="300"/></svg>',
                encoding="utf-8",
            )
            config["banner"] = {"path": "docs/assets/banner.svg", "alt": "Configured banner"}
        (docs / "docsprout.json").write_text(json.dumps(config), encoding="utf-8")
        (docs / "layout.json").write_text(json.dumps({
            "schema_version": 1,
            "navigation": [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}]}],
        }), encoding="utf-8")

    def test_prose_images_shrink_without_enlarging_small_images(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root)

            build_site(root=root, output=root / "site", release="preview")

            css = (root / "site" / "assets" / "site.css").read_text(encoding="utf-8")
            prose_images = _declarations(css, ".prose img")
            self.assertEqual("100%", prose_images["max-width"])
            self.assertEqual("auto", prose_images["height"])
            self.assertNotIn("width", prose_images)
            self.assertNotIn("display", prose_images)
            self.assertNotRegex(css, r"(?:^|})img\{")

            page = (root / "site" / "index.html").read_text(encoding="utf-8")
            self.assertIn(
                '<img src="assets/content/assets/oversized.svg" alt="Oversized illustration">',
                page,
            )
            self.assertIn('<img src="assets/content/assets/badge.svg" alt="Small badge">', page)

    def test_configured_banner_keeps_its_existing_responsive_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root, banner=True)

            build_site(root=root, output=root / "site", release="preview")

            css = (root / "site" / "assets" / "site.css").read_text(encoding="utf-8")
            banner = _declarations(css, ".banner")
            self.assertEqual("100%", banner["max-width"])
            self.assertEqual("100%", banner["width"])
            self.assertEqual("auto", banner["height"])
            self.assertEqual("cover", banner["object-fit"])
            page = (root / "site" / "index.html").read_text(encoding="utf-8")
            self.assertIn('class="banner" src="assets/banner.svg"', page)

    def test_custom_css_can_override_the_default_after_docsprout_styles(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            custom = ".prose img{max-width:none;height:auto}"
            self._project(root, custom_css=custom)

            build_site(root=root, output=root / "site", release="preview")

            page = (root / "site" / "index.html").read_text(encoding="utf-8")
            site_css = page.index('href="assets/site.css"')
            custom_link = page.index('href="assets/custom.css"')
            self.assertGreater(custom_link, site_css)
            self.assertEqual(custom, (root / "site" / "assets" / "custom.css").read_text(encoding="utf-8"))

    def test_all_build_modes_use_the_same_responsive_core_asset(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root)

            normal = root / "normal"
            single = root / "single"
            build_site(root=root, output=normal, release="preview")
            build_site(root=root, output=single, release="0.18.1")
            normal_css = (normal / "assets" / "site.css").read_text(encoding="utf-8")
            self.assertEqual(SITE_CSS, normal_css)
            self.assertEqual(normal_css, (single / "assets" / "site.css").read_text(encoding="utf-8"))

            self._git(root, "init")
            self._git(root, "config", "user.email", "tests@example.test")
            self._git(root, "config", "user.name", "Tests")
            self._git(root, "add", "docs")
            self._git(root, "commit", "-m", "v1")
            self._git(root, "tag", "v1.0.0")
            (root / "docs" / "index.md").write_text("# Current\n\nThe current image fixture.\n", encoding="utf-8")
            (root / "docs" / "versions.json").write_text(json.dumps({
                "schema_version": 1,
                "current": "2.0.0",
                "versions": [
                    {"release": "2.0.0", "source_ref": "v2.0.0"},
                    {"release": "1.0.0", "source_ref": "v1.0.0"},
                ],
            }), encoding="utf-8")
            self._git(root, "add", "docs")
            self._git(root, "commit", "-m", "v2")
            self._git(root, "tag", "v2.0.0")

            versioned = root / "versioned"
            build_all(root=root, output=versioned)
            for release in ("1.0.0", "2.0.0"):
                versioned_css = (versioned / release / "assets" / "site.css").read_text(encoding="utf-8")
                self.assertEqual(SITE_CSS, versioned_css, release)

    def test_responsive_rule_survives_theme_and_content_width_settings(self) -> None:
        for theme_style, content_width in (("paper", "compact"), ("glassmorphic", "wide")):
            with self.subTest(theme_style=theme_style, content_width=content_width), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self._project(root, theme_style=theme_style, content_width=content_width)

                build_site(root=root, output=root / "site", release="preview")

                page = (root / "site" / "index.html").read_text(encoding="utf-8")
                self.assertIn(f'data-visual-theme="{theme_style}"', page)
                self.assertIn(f'data-content-width="{content_width}"', page)
                css = (root / "site" / "assets" / "site.css").read_text(encoding="utf-8")
                self.assertEqual("100%", _declarations(css, ".prose img")["max-width"])

    def test_maintained_visual_fixture_carries_oversized_and_small_images(self) -> None:
        fixture = Path(__file__).resolve().parents[1] / "examples" / "visual-fixtures"
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "site"
            build_site(root=fixture, output=output, release="fixture")

            page = (output / "index.html").read_text(encoding="utf-8")
            for source_name in ("oversized-prose-image.svg", "small-badge.svg"):
                self.assertIn(f"assets/content/assets/{source_name}", page)
                self.assertTrue((output / "assets" / "content" / "assets" / source_name).is_file())
            css = (output / "assets" / "site.css").read_text(encoding="utf-8")
            self.assertEqual("100%", _declarations(css, ".prose img")["max-width"])

    @staticmethod
    def _git(root: Path, *arguments: str) -> None:
        subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True, text=True)
