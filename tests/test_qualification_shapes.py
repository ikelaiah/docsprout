"""Qualification: representative repository shapes build publishable sites.

One small, explicit fixture per real-world repository shape that DocSprout
claims to support. Every test asserts meaningful generated output, not just a
successful exit.
"""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from docsprout.build import build_site
from docsprout.errors import DocSproutError


def _project(root: Path, *, name: str = "Demo") -> None:
    docs = root / "docs"
    docs.mkdir(parents=True)
    (docs / "docsprout.json").write_text(
        json.dumps({"schema_version": 1, "project": {"name": name}}), encoding="utf-8",
    )


def _layout(root: Path, navigation: list[dict], *, home: dict | None = None, unlisted: str | None = "exclude") -> None:
    layout: dict = {"schema_version": 1, "navigation": navigation}
    if home is not None:
        layout["home"] = home
    if unlisted is not None:
        layout["unlisted"] = unlisted
    (root / "docs" / "layout.json").write_text(json.dumps(layout), encoding="utf-8")


def _pages(root: Path, *paths: str) -> None:
    for position, path in enumerate(paths):
        page = root / "docs" / path
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(f"# {Path(path).stem.replace('-', ' ').title()}\n", encoding="utf-8")


def _build(root: Path) -> tuple[Path, object]:
    output = root / "site"
    result = build_site(root=root, output=output, release="qualification")
    return output, result


class RepositoryShapeQualificationTests(unittest.TestCase):
    def test_qualifies_a_repository_with_only_a_root_readme(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "readme-project"
            root.mkdir()
            _project(root)
            (root / "README.md").write_text("# Flagship README\n\nRead me first.\n", encoding="utf-8")
            _layout(root, [{"title": "Overview", "pages": [{"title": "Overview", "path": "README.md", "source": "root"}]}])

            output, result = _build(root)

            self.assertEqual(1, result.page_count)
            self.assertEqual("README.md", result.home_document)
            self.assertIn("Flagship README", (output / "index.html").read_text(encoding="utf-8"))

    def test_qualifies_a_repository_with_only_docs_index(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "index-project"
            root.mkdir()
            _project(root)
            _pages(root, "index.md")
            _layout(root, [{"title": "Documentation", "pages": [{"title": "Home", "path": "index.md"}]}])

            output, result = _build(root)

            self.assertEqual(1, result.page_count)
            self.assertTrue((output / "index.html").is_file())
            self.assertIn("Index", (output / "index.html").read_text(encoding="utf-8"))

    def test_qualifies_explicit_layout_home_selection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "explicit-home"
            root.mkdir()
            _project(root)
            _pages(root, "index.md", "guide.md")
            _layout(root, [{"title": "Docs", "pages": [{"title": "Index", "path": "index.md"}, {"title": "Guide", "path": "guide.md"}]}], home={"path": "guide.md"})

            output, result = _build(root)

            self.assertEqual("guide.md", result.home_document)
            self.assertIn("Guide", (output / "index.html").read_text(encoding="utf-8"))
            self.assertTrue((output / "docs-index.html").is_file())

    def test_qualifies_unlisted_exclude_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "unlisted-project"
            root.mkdir()
            _project(root)
            _pages(root, "index.md", "private.md")

            _layout(root, [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}]}], unlisted="exclude")
            output, result = _build(root)
            self.assertEqual(1, result.page_count)
            self.assertEqual(1, result.excluded_count)
            self.assertFalse((output / "private.html").exists())

            _layout(root, [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}]}], unlisted="error")
            with self.assertRaisesRegex(DocSproutError, "unlisted Markdown document"):
                build_site(root=root, output=root / "site", release="qualification")

    def test_qualifies_nested_documentation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "nested-project"
            root.mkdir()
            _project(root)
            _pages(root, "index.md", "guides/beginner.md", "guides/advanced/configuration.md")
            _layout(root, [
                {"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]},
                {"title": "Guides", "pages": [
                    {"title": "Beginner", "path": "guides/beginner.md"},
                    {"title": "Configuration", "path": "guides/advanced/configuration.md"},
                ]},
            ])

            output, result = _build(root)

            self.assertEqual(3, result.page_count)
            self.assertTrue((output / "guides" / "beginner.html").is_file())
            self.assertTrue((output / "guides" / "advanced" / "configuration.html").is_file())
            beginner = (output / "guides" / "beginner.html").read_text(encoding="utf-8")
            self.assertIn('href="advanced/configuration.html"', beginner)
            configuration = (output / "guides" / "advanced" / "configuration.html").read_text(encoding="utf-8")
            self.assertIn('href="../beginner.html"', configuration)

    def test_qualifies_local_assets_and_nested_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "assets-project"
            root.mkdir()
            _project(root)
            (root / "docs" / "assets").mkdir(parents=True)
            (root / "docs" / "guides" / "images").mkdir(parents=True)
            (root / "docs" / "assets" / "logo.svg").write_text("<svg/>", encoding="utf-8")
            (root / "docs" / "guides" / "images" / "diagram.svg").write_text("<svg/>", encoding="utf-8")
            (root / "docs" / "index.md").write_text("# Assets\n\n![Logo](assets/logo.svg)\n", encoding="utf-8")
            (root / "docs" / "guides" / "advanced.md").write_text("# Advanced\n\n![Diagram](images/diagram.svg)\n", encoding="utf-8")
            _layout(root, [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}, {"title": "Advanced", "path": "guides/advanced.md"}]}])

            output, _ = _build(root)

            self.assertTrue((output / "assets" / "content" / "assets" / "logo.svg").is_file())
            self.assertTrue((output / "assets" / "content" / "guides" / "images" / "diagram.svg").is_file())
            self.assertIn('src="assets/content/assets/logo.svg"', (output / "index.html").read_text(encoding="utf-8"))

    def test_qualifies_paths_containing_spaces(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "spaces-project"
            root.mkdir()
            _project(root)
            (root / "docs" / "user guides").mkdir(parents=True)
            (root / "docs" / "index.md").write_text("# Home\n\n[Getting started](getting started.md)\n", encoding="utf-8")
            (root / "docs" / "getting started.md").write_text("# Getting started\n\n[User guides](user guides/install notes.md)\n", encoding="utf-8")
            (root / "docs" / "user guides" / "install notes.md").write_text("# Install notes\n", encoding="utf-8")
            _layout(root, [{"title": "Docs", "pages": [
                {"title": "Home", "path": "index.md"},
                {"title": "Getting Started", "path": "getting started.md"},
                {"title": "Install Notes", "path": "user guides/install notes.md"},
            ]}])

            output, result = _build(root)

            self.assertEqual(3, result.page_count)
            self.assertTrue((output / "getting started.html").is_file())
            self.assertTrue((output / "user guides" / "install notes.html").is_file())
            home = (output / "index.html").read_text(encoding="utf-8")
            self.assertIn('href="getting started.html"', home)
            search = json.loads((output / "search-index.json").read_text(encoding="utf-8"))
            self.assertIn("user guides/install notes.html", [entry["url"] for entry in search["entries"]])

    def test_qualifies_unicode_document_names_and_anchors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "unicode-project"
            root.mkdir()
            _project(root)
            (root / "docs" / "index.md").write_text("# Übungs-Home\n\n[Prüfungshinweise](prüfungshinweise.md)\n", encoding="utf-8")
            (root / "docs" / "prüfungshinweise.md").write_text("# Prüfungshinweise\n\n## Übungsdetails\n\nContent.\n", encoding="utf-8")
            _layout(root, [{"title": "Info", "pages": [{"title": "Home", "path": "index.md"}, {"title": "Prüfungshinweise", "path": "prüfungshinweise.md"}]}])

            output, result = _build(root)

            self.assertEqual(2, result.page_count)
            self.assertTrue((output / "prüfungshinweise.html").is_file())
            page = (output / "prüfungshinweise.html").read_text(encoding="utf-8")
            self.assertIn('id="übungsdetails"', page)
            self.assertIn('href="#übungsdetails"', page)

    def test_qualifies_a_repository_path_containing_spaces(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "my project docs"
            root.mkdir()
            (root / "README.md").write_text("# Project with spaces\n", encoding="utf-8")
            _project(root)
            _layout(root, [{"title": "Overview", "pages": [{"title": "Overview", "path": "README.md", "source": "root"}]}])

            output, result = _build(root)

            self.assertEqual(1, result.page_count)
            self.assertIn("Project with spaces", (output / "index.html").read_text(encoding="utf-8"))

    def test_qualifies_multi_level_navigation_and_previous_next_chains(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "multi-nav-project"
            root.mkdir()
            _project(root)
            _pages(root, "index.md", "quick-start.md", "guides/one.md", "guides/two.md", "reference/api.md")
            _layout(root, [
                {"title": "Start", "pages": [{"title": "Home", "path": "index.md"}, {"title": "Quick Start", "path": "quick-start.md"}]},
                {"title": "Guides", "pages": [{"title": "Guide One", "path": "guides/one.md"}, {"title": "Guide Two", "path": "guides/two.md"}]},
                {"title": "Reference", "pages": [{"title": "API", "path": "reference/api.md"}]},
            ])

            output, result = _build(root)

            self.assertEqual(5, result.page_count)
            self.assertEqual(3, result.section_count)
            quick_start = (output / "quick-start.html").read_text(encoding="utf-8")
            self.assertIn('class="page-previous" href="index.html"', quick_start)
            self.assertIn('class="page-next" href="guides/one.html"', quick_start)
            api = (output / "reference" / "api.html").read_text(encoding="utf-8")
            self.assertIn('class="page-previous" href="../guides/two.html"', api)
            self.assertNotIn("page-next", api)
            sidebar = (output / "index.html").read_text(encoding="utf-8")
            sidebar_navigation = sidebar[sidebar.index('<nav class="sidebar"'):sidebar.index("</nav>")]
            self.assertEqual(3, sidebar_navigation.count("<h2>"))
            self.assertEqual(5, sidebar_navigation.count('<a class='))

    def test_qualifies_a_root_readme_alongside_docs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "readme-plus-docs"
            root.mkdir()
            (root / "README.md").write_text("# Repository overview\n\n[Guides](docs/guides.md)\n", encoding="utf-8")
            _project(root)
            _pages(root, "index.md", "guides.md")
            _layout(root, [
                {"title": "Overview", "pages": [{"title": "Overview", "path": "README.md", "source": "root"}]},
                {"title": "Documentation", "pages": [{"title": "Index", "path": "index.md"}, {"title": "Guides", "path": "guides.md"}]},
            ])

            output, result = _build(root)

            self.assertEqual(3, result.page_count)
            self.assertEqual("README.md", result.home_document)
            self.assertTrue((output / "docs-index.html").is_file())
            self.assertIn("Repository overview", (output / "index.html").read_text(encoding="utf-8"))
            self.assertTrue((output / "guides.html").is_file())

    def test_qualifies_ancillary_markdown_is_never_published_by_surprise(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "ancillary-project"
            root.mkdir()
            _project(root)
            _pages(root, "index.md")
            for name in ("CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md"):
                (root / name).write_text(f"# {name}\n", encoding="utf-8")
            _layout(root, [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}]}])

            output, result = _build(root)

            self.assertEqual(1, result.page_count)
            for name in ("CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md"):
                self.assertFalse((output / name.replace(".md", ".html")).exists())

    def test_qualifies_a_generic_non_pascal_repository_shape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "generic-project"
            root.mkdir()
            (root / "pyproject.toml").write_text("[project]\nname = 'generic-project'\n", encoding="utf-8")
            (root / "src" / "generic_project").mkdir(parents=True)
            (root / "src" / "generic_project" / "core.py").write_text("VALUE = 1\n", encoding="utf-8")
            (root / "README.md").write_text("# generic-project\n", encoding="utf-8")
            _project(root, name="generic-project")
            (root / "docs" / "index.md").write_text(
                "# Home\n\n```python\nfrom generic_project import core\nprint(core.VALUE)\n```\n", encoding="utf-8"
            )
            _layout(root, [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}]}])

            output, result = _build(root)

            self.assertEqual(1, result.page_count)
            self.assertIn('class="language-python syntax-highlight"', (output / "index.html").read_text(encoding="utf-8"))

    def test_qualifies_a_pascal_oriented_repository_shape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "fp-project"
            root.mkdir()
            (root / "src" / "units").mkdir(parents=True)
            (root / "src" / "units" / "matrixmath.pas").write_text("unit MatrixMath;\n", encoding="utf-8")
            (root / "README.md").write_text("# fp-project\n\nDocumentation for a Free Pascal library.\n", encoding="utf-8")
            _project(root, name="fp-project")
            (root / "docs" / "index.md").write_text("# Home\n", encoding="utf-8")
            (root / "docs" / "units-reference.md").write_text(
                "# Units reference\n\n```pascal\nuses MatrixMath;\nvar m: TMatrix;\n```\n", encoding="utf-8"
            )
            _layout(root, [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}, {"title": "Units Reference", "path": "units-reference.md"}]}])

            output, result = _build(root)

            self.assertEqual(2, result.page_count)
            page = (output / "units-reference.html").read_text(encoding="utf-8")
            self.assertIn('class="language-pascal syntax-highlight"', page)
            self.assertIn('prefers-reduced-motion', (output / "assets" / "site.css").read_text(encoding="utf-8"))

    def test_qualifies_a_repository_with_only_unlisted_documents_instead_of_failing_quietly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "empty-navigation-project"
            root.mkdir()
            _project(root)
            _pages(root, "index.md", "draft.md")
            _layout(root, [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}]}], unlisted="exclude")

            output, result = _build(root)

            self.assertEqual(1, result.page_count)
            self.assertEqual(1, result.excluded_count)
            self.assertFalse((output / "draft.html").exists())