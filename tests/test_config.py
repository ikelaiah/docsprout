import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from docsprout.config import load_config
from docsprout.errors import DocSproutError


class ConfigurationDiagnosticsTests(unittest.TestCase):
    def _write_config(self, root: Path, document: dict, layout: dict) -> None:
        docs = root / "docs"
        docs.mkdir()
        (docs / "index.md").write_text("# Home", encoding="utf-8")
        (docs / "docsprout.json").write_text(json.dumps(document), encoding="utf-8")
        (docs / "layout.json").write_text(json.dumps(layout), encoding="utf-8")

    def test_explains_how_to_fix_an_invalid_accent_colour(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {"schema_version": 1, "project": {"name": "Demo"}, "theme": {"accent": "blue"}},
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            with self.assertRaisesRegex(DocSproutError, r"theme\.accent.*Use a #RRGGBB colour"):
                load_config(root)

    def test_names_the_section_and_next_step_for_an_empty_navigation_group(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {"schema_version": 1, "project": {"name": "Demo"}},
                {"schema_version": 1, "navigation": [{"title": "Guides", "pages": []}]},
            )

            with self.assertRaisesRegex(DocSproutError, r"section 'Guides'.*Add at least one page"):
                load_config(root)

    def test_explains_how_to_fix_a_missing_navigation_document(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {"schema_version": 1, "project": {"name": "Demo"}},
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Install", "path": "install.md"}]}]},
            )

            with self.assertRaisesRegex(DocSproutError, r"navigation page 'install\.md'.*Create docs/install\.md or correct its path"):
                load_config(root)

    def test_loads_a_colour_preset_and_supported_project_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {
                    "schema_version": 1,
                    "project": {"name": "Demo"},
                    "theme": {"preset": "purple"},
                    "identity": {
                        "footer": "Built for Pascal maintainers.",
                        "links": [{"label": "Source code", "url": "https://example.test/source"}],
                    },
                },
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            config = load_config(root)

            self.assertEqual("#7c3aed", config.accent)
            self.assertEqual("Built for Pascal maintainers.", config.footer)
            self.assertEqual((("Source code", "https://example.test/source"),), config.project_links)

    def test_uses_an_explicit_listed_home_page(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(root, {"schema_version": 1, "project": {"name": "Demo"}}, {"schema_version": 1, "home": {"path": "guide.md"}, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}, {"title": "Guide", "path": "guide.md"}]}]})
            (root / "docs" / "guide.md").write_text("# Guide", encoding="utf-8")
            self.assertEqual("guide.md", load_config(root).home_document)

    def test_uses_an_explicit_listed_repository_root_readme_as_home(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(root, {"schema_version": 1, "project": {"name": "Demo"}}, {"schema_version": 1, "unlisted": "exclude", "home": {"path": "README.md", "source": "root"}, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "README.md", "source": "root"}]}]})
            (root / "README.md").write_text("# Root home", encoding="utf-8")
            self.assertEqual("README.md", load_config(root).home_document)

    def test_rejects_an_unlisted_or_invalid_explicit_home_page(self) -> None:
        for home, message in (({"path": "missing.md"}, "home.path.*listed navigation page"), ({"path": "README.md", "source": "docs"}, "home.*source.*root"), ({"path": "index.md", "source": "root"}, "repository-root source only supports README.md")):
            with self.subTest(home=home), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self._write_config(root, {"schema_version": 1, "project": {"name": "Demo"}}, {"schema_version": 1, "home": home, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]})
                with self.assertRaisesRegex(DocSproutError, message):
                    load_config(root)

    def test_loads_a_repository_local_identity_logo(self) -> None:
        for suffix, contents in ((".svg", "<svg></svg>"), (".png", b"png")):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                logo = f"docs/assets/logo{suffix}"
                self._write_config(
                    root,
                    {
                        "schema_version": 1,
                        "project": {"name": "Demo"},
                        "identity": {"logo": logo},
                    },
                    {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
                )
                asset = root / logo
                asset.parent.mkdir()
                if isinstance(contents, bytes):
                    asset.write_bytes(contents)
                else:
                    asset.write_text(contents, encoding="utf-8")

                self.assertEqual(logo, load_config(root).logo)

    def test_rejects_unsafe_or_unsupported_identity_logo_paths(self) -> None:
        cases = (
            ("../logo.svg", "identity.logo path is unsafe"),
            ("docs/assets/logo.jpg", "identity.logo must reference an SVG or PNG"),
        )
        for logo, message in cases:
            with self.subTest(logo=logo), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self._write_config(
                    root,
                    {"schema_version": 1, "project": {"name": "Demo"}, "identity": {"logo": logo}},
                    {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
                )
                if logo.endswith(".jpg"):
                    asset = root / "docs" / "assets" / "logo.jpg"
                    asset.parent.mkdir()
                    asset.write_bytes(b"not an image")

                with self.assertRaisesRegex(DocSproutError, message):
                    load_config(root)

    def test_loads_a_supported_visual_theme(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {"schema_version": 1, "project": {"name": "Demo"}, "theme": {"style": "midnight"}},
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            self.assertEqual("midnight", load_config(root).theme_style)

    def test_loads_a_supported_content_width(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {
                    "schema_version": 1,
                    "project": {"name": "Demo"},
                    "layout": {"content_width": "wide"},
                },
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            self.assertEqual("wide", load_config(root).content_width)

    def test_rejects_an_unknown_content_width_with_supported_names(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {
                    "schema_version": 1,
                    "project": {"name": "Demo"},
                    "layout": {"content_width": "fluid"},
                },
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            with self.assertRaisesRegex(DocSproutError, r"layout\.content_width.*compact, comfortable, wide"):
                load_config(root)

    def test_loads_homepage_cards_and_section_switches(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {
                    "schema_version": 1,
                    "project": {"name": "Demo"},
                    "homepage": {
                        "capabilities": [
                            {"title": "API reference", "description": "Every public unit."},
                            {"title": "Offline", "description": "No CDN."},
                        ],
                        "sections": {
                            "capabilities": True,
                            "banner": False,
                            "introduction": False,
                            "release_context": True,
                        },
                    },
                },
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            homepage = load_config(root).homepage

            self.assertEqual(("API reference", "Every public unit."), homepage.capabilities[0])
            self.assertFalse(homepage.show_banner)
            self.assertFalse(homepage.show_introduction)
            self.assertTrue(homepage.show_release_context)

    def test_names_an_invalid_homepage_card_field_and_correction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {
                    "schema_version": 1,
                    "project": {"name": "Demo"},
                    "homepage": {"capabilities": [{"title": "", "description": "Useful."}]},
                },
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            with self.assertRaisesRegex(DocSproutError, r"homepage\.capabilities\[0\]\.title.*Use a non-empty string"):
                load_config(root)

    def test_names_an_invalid_homepage_section_field_and_correction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {
                    "schema_version": 1,
                    "project": {"name": "Demo"},
                    "homepage": {"sections": {"banner": "no"}},
                },
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            with self.assertRaisesRegex(DocSproutError, r"homepage\.sections\.banner.*Use true or false"):
                load_config(root)

    def test_rejects_an_unknown_homepage_section_with_the_supported_names(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {
                    "schema_version": 1,
                    "project": {"name": "Demo"},
                    "homepage": {"sections": {"introducton": False}},
                },
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            with self.assertRaisesRegex(DocSproutError, r"homepage\.sections\.introducton.*Use one of"):
                load_config(root)

    def test_names_unlisted_modern_markdown_and_how_to_include_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {"schema_version": 1, "project": {"name": "Demo"}},
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )
            (root / "docs" / "reference.md").write_text("# Reference", encoding="utf-8")

            with self.assertRaisesRegex(DocSproutError, r"unlisted Markdown document 'reference\.md'.*Add it to navigation"):
                load_config(root)

    def test_explicit_error_policy_retains_strict_unlisted_markdown_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {"schema_version": 1, "project": {"name": "Demo"}},
                {"schema_version": 1, "unlisted": "error", "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )
            (root / "docs" / "private.md").write_text("# Private", encoding="utf-8")

            with self.assertRaisesRegex(DocSproutError, r"unlisted Markdown document 'private\.md'"):
                load_config(root)

    def test_exclude_policy_allows_unlisted_markdown_without_publishing_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {"schema_version": 1, "project": {"name": "Demo"}},
                {"schema_version": 1, "unlisted": "exclude", "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )
            (root / "docs" / "private.md").write_text("# Private", encoding="utf-8")

            config = load_config(root)

            self.assertEqual(("private.md",), config.excluded_documents)

    def test_rejects_an_unknown_unlisted_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {"schema_version": 1, "project": {"name": "Demo"}},
                {"schema_version": 1, "unlisted": "include", "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            with self.assertRaisesRegex(DocSproutError, r"unlisted.*'error' or 'exclude'"):
                load_config(root)

    def test_explains_the_schema_compatibility_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {"schema_version": 2, "project": {"name": "Demo"}},
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            with self.assertRaisesRegex(DocSproutError, r"schema version 1.*migration"):
                load_config(root)

    def test_rejects_an_unknown_theme_field_with_a_typo_suggestion(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {"schema_version": 1, "project": {"name": "Demo"}, "theme": {"presett": "purple"}},
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )

            with self.assertRaisesRegex(DocSproutError, r"Unknown field 'theme\.presett'\. Did you mean 'theme\.preset'\?"):
                load_config(root)

    def test_rejects_unknown_fields_across_all_documented_schema_one_objects(self) -> None:
        valid_layout = {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]}
        bad_documents = (
            {"schema_version": 1, "project": {"name": "Demo"}, "them": {"preset": "purple"}},
            {"schema_version": 1, "project": {"name": "Demo", "descriptionn": "text"}},
            {"schema_version": 1, "project": {"name": "Demo"}, "layout": {"width": "wide"}},
            {"schema_version": 1, "project": {"name": "Demo"}, "banner": {"path": "x", "alt": "y", "scale": 2}},
            {"schema_version": 1, "project": {"name": "Demo"}, "identity": {"logos": "docs/assets/x.svg"}},
            {"schema_version": 1, "project": {"name": "Demo"}, "homepage": {"capabiliti": []}},
            {"schema_version": 1, "project": {"name": "Demo"}, "homepage": {"capabilities": [{"title": "T", "description": "D", "icon": "x"}]}},
        )
        for index, document in enumerate(bad_documents):
            with self.subTest(document=index), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self._write_config(root, document, valid_layout)
                with self.assertRaisesRegex(DocSproutError, r"Unknown field"):
                    load_config(root)
        bad_layouts = (
            {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}], "extras": True},
            {"schema_version": 1, "home": {"path": "index.md", "target": "x"}, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md", "target": "x"}]}]},
            {"schema_version": 1, "navigation": [{"title": "Start", "folded": True, "pages": [{"title": "Home", "path": "index.md"}]}]},
        )
        for index, layout in enumerate(bad_layouts):
            with self.subTest(layout=index), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self._write_config(root, {"schema_version": 1, "project": {"name": "Demo"}}, layout)
                with self.assertRaisesRegex(DocSproutError, r"Unknown field"):
                    load_config(root)

    def test_rejects_an_empty_navigation_page_or_section_title(self) -> None:
        for layout, message in (
            ({"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "", "path": "index.md"}]}]}, "non-empty title"),
            ({"schema_version": 1, "navigation": [{"title": "  ", "pages": [{"title": "Home", "path": "index.md"}]}]}, "non-empty title"),
        ):
            with self.subTest(layout=layout), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self._write_config(root, {"schema_version": 1, "project": {"name": "Demo"}}, layout)
                with self.assertRaisesRegex(DocSproutError, message):
                    load_config(root)

    def test_rejects_non_string_project_metadata_fields(self) -> None:
        for field, value in (("description", 42), ("repository_url", ["x"]), ("site_url", None)):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self._write_config(
                    root,
                    {"schema_version": 1, "project": {"name": "Demo", field: value}},
                    {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
                )
                if field == "site_url":
                    config = load_config(root)
                    self.assertIsNone(config.site_url)
                else:
                    with self.assertRaisesRegex(DocSproutError, rf"project\.{field}.*string"):
                        load_config(root)

    def test_allows_only_the_exact_repository_root_readme_as_an_explicit_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (root / "README.md").write_text("# Root", encoding="utf-8")
            (docs / "docsprout.json").write_text(json.dumps({"schema_version": 1, "project": {"name": "Demo"}}), encoding="utf-8")
            layout = {"schema_version": 1, "navigation": [{"title": "Overview", "pages": [
                {"title": "Overview", "path": "README.md", "source": "root"},
            ]}]}
            (docs / "layout.json").write_text(json.dumps(layout), encoding="utf-8")

            config = load_config(root)
            self.assertEqual("root", config.pages[0].source)

            layout["navigation"][0]["pages"][0]["path"] = "../README.md"
            (docs / "layout.json").write_text(json.dumps(layout), encoding="utf-8")
            with self.assertRaisesRegex(DocSproutError, "invalid Markdown path"):
                load_config(root)

            layout["navigation"][0]["pages"][0]["path"] = "CHANGELOG.md"
            (docs / "layout.json").write_text(json.dumps(layout), encoding="utf-8")
            with self.assertRaisesRegex(DocSproutError, "repository-root source only supports README.md"):
                load_config(root)

    def test_rejects_a_docs_symlink_that_resolves_outside_the_repository(self) -> None:
        with tempfile.TemporaryDirectory() as temporary, tempfile.TemporaryDirectory() as external:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            outside = Path(external) / "outside.md"
            outside.write_text("# Outside", encoding="utf-8")
            page_path = "outside.md"
            try:
                (docs / "outside.md").symlink_to(outside)
            except (NotImplementedError, OSError) as error:
                if os.name != "nt":
                    self.skipTest(f"symlink creation is unavailable: {error}")
                # Windows without Developer Mode cannot create file symlinks, but
                # unprivileged directory junctions use the same resolve()-based
                # outside-the-repository guard, so qualify the escape resistance
                # through a junctioned directory.
                junction = docs / "outside"
                try:
                    subprocess.run(
                        ["cmd", "/c", "mklink", "/J", str(junction), str(Path(external))],
                        check=True, capture_output=True,
                    )
                except (OSError, subprocess.CalledProcessError) as junction_error:
                    self.skipTest(f"neither symlink nor junction creation is available: {error}; {junction_error}")
                page_path = "outside/outside.md"
            (docs / "docsprout.json").write_text(json.dumps({"schema_version": 1, "project": {"name": "Demo"}}), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({"schema_version": 1, "navigation": [{"title": "Docs", "pages": [
                {"title": "Outside", "path": page_path},
            ]}]}), encoding="utf-8")

            with self.assertRaisesRegex(DocSproutError, "outside the repository root"):
                load_config(root)

    def test_loads_a_legacy_dockit_json_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Home", encoding="utf-8")
            (docs / "dockit.json").write_text(
                json.dumps({"schema_version": 1, "project": {"name": "Legacy"}}), encoding="utf-8",
            )
            (docs / "layout.json").write_text(json.dumps({
                "schema_version": 1,
                "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}],
            }), encoding="utf-8")

            config = load_config(root)

            self.assertEqual("Legacy", config.name)

    def test_rejects_both_configuration_filenames_with_an_actionable_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_config(
                root,
                {"schema_version": 1, "project": {"name": "Current"}},
                {"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]},
            )
            (root / "docs" / "dockit.json").write_text(
                json.dumps({"schema_version": 1, "project": {"name": "Legacy"}}), encoding="utf-8",
            )

            with self.assertRaisesRegex(DocSproutError, r"both docsprout\.json and dockit\.json exist"):
                load_config(root)

    def test_legacy_dockit_json_diagnostics_use_the_legacy_file_name(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Home", encoding="utf-8")
            (docs / "dockit.json").write_text(
                json.dumps({"schema_version": 1, "project": {"name": "Legacy"}, "them": {}}), encoding="utf-8",
            )
            (docs / "layout.json").write_text(
                json.dumps({"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]}),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(DocSproutError, r"Unknown field 'dockit\.them'"):
                load_config(root)

    def test_canonical_configuration_diagnostics_use_the_canonical_file_name(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Home", encoding="utf-8")
            (docs / "docsprout.json").write_text(
                json.dumps({"schema_version": 1, "project": {"name": "Current"}, "them": {}}), encoding="utf-8",
            )
            (docs / "layout.json").write_text(
                json.dumps({"schema_version": 1, "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]}),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(DocSproutError, r"Unknown field 'docsprout\.them'"):
                load_config(root)
