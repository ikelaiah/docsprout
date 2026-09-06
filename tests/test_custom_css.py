import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from dockit_fp.build import build_site
from dockit_fp.config import load_config
from dockit_fp.errors import DocKitError
from dockit_fp.versions import build_all


class CustomCssTests(unittest.TestCase):
    def _project(
        self, root: Path, *, nested: bool = True, custom_css: str = "docs/assets/custom.css",
    ) -> None:
        docs = root / "docs"
        (docs / "assets").mkdir(parents=True)
        (docs / "index.md").write_text("# Home\n\n[Guide](guides/deep.md)", encoding="utf-8")
        if nested:
            (docs / "guides").mkdir()
            (docs / "guides" / "deep.md").write_text("# Deep\n\n[Back](../index.md)", encoding="utf-8")
        (docs / "assets" / "custom.css").write_text(
            ".prose h1{color:rebeccapurple}.prose{--dk-accent:#7c3aed}", encoding="utf-8"
        )
        (docs / "dockit.json").write_text(json.dumps({
            "schema_version": 1, "project": {"name": "Demo"}, "theme": {"custom_css": custom_css},
        }), encoding="utf-8")
        pages = [{"title": "Home", "path": "index.md"}]
        if nested:
            pages.append({"title": "Deep", "path": "guides/deep.md"})
        (docs / "layout.json").write_text(json.dumps({
            "schema_version": 1, "unlisted": "exclude",
            "navigation": [{"title": "Docs", "pages": pages}],
        }), encoding="utf-8")

    def test_loads_a_valid_repository_local_custom_css_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root)

            config = load_config(root)

            self.assertEqual("docs/assets/custom.css", config.custom_css)

    def test_copies_custom_css_deterministically_and_loads_it_after_dockit_styles(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root)

            build_site(root=root, output=root / "site", release="dev")

            copied = root / "site" / "assets" / "custom.css"
            self.assertEqual(
                ".prose h1{color:rebeccapurple}.prose{--dk-accent:#7c3aed}",
                copied.read_text(encoding="utf-8"),
            )
            home = (root / "site" / "index.html").read_text(encoding="utf-8")
            site_css = home.index('href="assets/site.css"')
            katex_css = home.index('href="assets/katex/katex.min.css"')
            custom_link = home.index('href="assets/custom.css"')
            self.assertGreater(custom_link, site_css, "custom CSS must load after site.css")
            self.assertGreater(custom_link, katex_css, "custom CSS must load after KaTeX styles")

    def test_nested_pages_reference_custom_css_with_a_working_relative_route(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root)

            build_site(root=root, output=root / "site", release="dev")

            deep = (root / "site" / "guides" / "deep.html").read_text(encoding="utf-8")
            self.assertIn('href="../assets/custom.css"', deep)
            self.assertTrue((root / "site" / "assets" / "custom.css").is_file())

    def test_custom_css_is_optional_and_absent_without_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root)
            (root / "docs" / "dockit.json").write_text(json.dumps({
                "schema_version": 1, "project": {"name": "Demo"},
            }), encoding="utf-8")

            build_site(root=root, output=root / "site", release="dev")

            home = (root / "site" / "index.html").read_text(encoding="utf-8")
            self.assertNotIn("custom.css", home)
            self.assertFalse((root / "site" / "assets" / "custom.css").exists())

    def test_rejects_a_missing_custom_css_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root, custom_css="docs/assets/missing.css")

            with self.assertRaisesRegex(DocKitError, "does not exist"):
                load_config(root)

    def test_rejects_a_non_css_custom_css_extension(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root, custom_css="docs/assets/custom.txt")
            (root / "docs" / "assets" / "custom.txt").write_text("not css", encoding="utf-8")

            with self.assertRaisesRegex(DocKitError, r"\.css file"):
                load_config(root)

    def test_rejects_absolute_and_traversing_custom_css_paths(self) -> None:
        cases = (
            ("C:/outside/custom.css", "unsafe"),
            ("../custom.css", "unsafe"),
        )
        for value, message in cases:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self._project(root, custom_css=value)

                with self.assertRaisesRegex(DocKitError, message):
                    load_config(root)

    def test_rejects_a_custom_css_symlink_that_escapes_the_repository(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, tempfile.TemporaryDirectory() as external_temporary:
            root = Path(temporary)
            external = Path(external_temporary) / "outside.css"
            external.write_text("body{}", encoding="utf-8")
            configured = "docs/assets/linked.css"
            self._project(root, custom_css=configured)
            target = root / "docs" / "assets" / "linked.css"
            try:
                target.symlink_to(external)
            except (NotImplementedError, OSError) as error:
                if os.name != "nt":
                    self.skipTest(f"symlink creation is unavailable: {error}")
                # Windows without Developer Mode cannot create file symlinks, but
                # unprivileged directory junctions exercise the same resolve()-based
                # outside-the-repository guard, so qualify the escape resistance
                # through a junctioned directory.
                junction = root / "docs" / "assets" / "css-outside"
                try:
                    subprocess.run(
                        ["cmd", "/c", "mklink", "/J", str(junction), str(Path(external_temporary))],
                        check=True, capture_output=True,
                    )
                except (OSError, subprocess.CalledProcessError) as junction_error:
                    self.skipTest(f"neither symlink nor junction creation is available: {error}; {junction_error}")
                configured = "docs/assets/css-outside/outside.css"
                (root / "docs" / "dockit.json").write_text(json.dumps({
                    "schema_version": 1,
                    "project": {"name": "Demo"},
                    "theme": {"custom_css": configured},
                }), encoding="utf-8")

            with self.assertRaisesRegex(DocKitError, "outside the repository root"):
                load_config(root)

    def test_versioned_builds_include_repository_local_custom_css(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            (docs / "assets").mkdir(parents=True)
            (docs / "index.md").write_text("# Version one", encoding="utf-8")
            (docs / "assets" / "custom.css").write_text(".prose h1{color:rebeccapurple}", encoding="utf-8")
            (docs / "dockit.json").write_text(json.dumps({
                "schema_version": 1, "project": {"name": "Demo"}, "theme": {"custom_css": "docs/assets/custom.css"},
            }), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({
                "schema_version": 1, "navigation": [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}]}],
            }), encoding="utf-8")
            self._git(root, "init")
            self._git(root, "config", "user.email", "tests@example.test")
            self._git(root, "config", "user.name", "Tests")
            self._git(root, "add", ".")
            self._git(root, "commit", "-m", "v1")
            self._git(root, "tag", "v1.0.0")
            (docs / "index.md").write_text("# Version two", encoding="utf-8")
            (docs / "assets" / "custom.css").write_text(".prose h1{color:mediumpurple}", encoding="utf-8")
            (docs / "versions.json").write_text(json.dumps({
                "schema_version": 1, "current": "2.0.0", "versions": [
                    {"release": "2.0.0", "source_ref": "v2.0.0"},
                    {"release": "1.0.0", "source_ref": "v1.0.0"},
                ],
            }), encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-m", "v2")
            self._git(root, "tag", "v2.0.0")

            build_all(root=root, output=root / "site")

            for release, colour in (("1.0.0", "rebeccapurple"), ("2.0.0", "mediumpurple")):
                css = root / "site" / release / "assets" / "custom.css"
                self.assertTrue(css.is_file(), release)
                self.assertIn(colour, css.read_text(encoding="utf-8"), release)
                page = (root / "site" / release / "index.html").read_text(encoding="utf-8")
                self.assertIn('href="assets/custom.css"', page, release)

    @staticmethod
    def _git(root: Path, *arguments: str) -> None:
        subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True, text=True)