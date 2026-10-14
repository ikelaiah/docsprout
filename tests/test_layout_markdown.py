import json
from pathlib import Path
import tempfile
import unittest

from docsprout.config import load_config
from docsprout.build import build_site
from docsprout.cli import _init
from docsprout.errors import DocSproutError


class MarkdownLayoutTests(unittest.TestCase):
    def make_project(self, root: Path) -> Path:
        docs = root / "docs"
        docs.mkdir()
        (docs / "docsprout.json").write_text(
            json.dumps({"schema_version": 1, "project": {"name": "Demo"}}), encoding="utf-8",
        )
        (docs / "index.md").write_text("# Home", encoding="utf-8")
        (docs / "guide.md").write_text("# Guide", encoding="utf-8")
        return docs

    def test_outline_matches_json_model_and_expands_only_the_group(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = self.make_project(root)
            (docs / "layout.md").write_text(
                "Layout-Version: 1\nHome: index.md\nUnlisted: exclude\n\n"
                "# Start here\n- [Overview](index.md)\n\n"
                "## Quickstart {expanded=true}\n  - [Guide](guide.md)\n",
                encoding="utf-8",
            )
            markdown = load_config(root)
            self.assertEqual((("Start here", "Quickstart"),), markdown.expanded_groups)
            self.assertEqual(("index.md", "guide.md"), tuple(page.path for page in markdown.pages))
            self.assertEqual("Quickstart", markdown.pages[1].subsection)

            (docs / "layout.md").unlink()
            (docs / "layout.json").write_text(json.dumps({
                "schema_version": 1, "home": {"path": "index.md"}, "unlisted": "exclude",
                "navigation": [{"title": "Start here", "pages": [
                    {"title": "Overview", "path": "index.md"},
                    {"title": "Quickstart", "expanded": True, "pages": [{"title": "Guide", "path": "guide.md"}]},
                ]}],
            }), encoding="utf-8")
            original = load_config(root)
            self.assertEqual(original.pages, markdown.pages)
            self.assertEqual(original.home_document, markdown.home_document)
            self.assertEqual(original.expanded_groups, markdown.expanded_groups)

    def test_root_readme_and_unlisted_layout_are_not_published(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = self.make_project(root)
            (root / "README.md").write_text("# Root", encoding="utf-8")
            (docs / "layout.md").write_text(
                "Layout-Version: 1\nHome: ../README.md\nUnlisted: exclude\n\n"
                "# Start\n- [Root](../README.md)\n- [Home](index.md)\n",
                encoding="utf-8",
            )
            config = load_config(root)
            self.assertEqual("README.md", config.home_document)
            self.assertEqual("root", config.pages[0].source)
            self.assertIn("guide.md", config.excluded_documents)
            self.assertNotIn("layout.md", config.excluded_documents)

    def test_root_and_docs_readmes_keep_distinct_layout_identities(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = self.make_project(root)
            (root / "README.md").write_text("# Project", encoding="utf-8")
            (docs / "README.md").write_text("# Documentation", encoding="utf-8")
            (docs / "layout.md").write_text(
                "Layout-Version: 1\nHome: ../README.md\nUnlisted: exclude\n"
                "# Start\n- [Project](../README.md)\n- [Documentation](README.md)\n",
                encoding="utf-8",
            )

            config = load_config(root)

            self.assertEqual([("root", "README.md"), ("docs", "README.md")], [
                (page.source, page.path) for page in config.pages
            ])
            self.assertEqual(("root", "README.md"), (config.home_source, config.home_document))

    def test_rejects_both_layouts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = self.make_project(root)
            (docs / "layout.md").write_text("Layout-Version: 1\n", encoding="utf-8")
            (docs / "layout.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(DocSproutError, "both layout.json and layout.md"):
                load_config(root)

    def test_reports_invalid_lines_and_group_attributes_with_line_numbers(self) -> None:
        for line, error in (
            ("## Quickstart {expand=true}", "unsupported group attribute"),
            ("### Too deep", "unsupported"),
            ("- [Bad](../private.md)", "invalid Markdown path"),
        ):
            with self.subTest(line=line), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                docs = self.make_project(root)
                (docs / "layout.md").write_text(
                    "Layout-Version: 1\nHome: index.md\nUnlisted: exclude\n"
                    "# Start\n- [Home](index.md)\n" + line + "\n",
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(DocSproutError, rf"layout\.md:6:.*{error}"):
                    load_config(root)

    def test_build_and_init_respect_existing_markdown_layout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = self.make_project(root)
            outline = (
                "Layout-Version: 1\nHome: index.md\nUnlisted: exclude\n\n"
                "# Start\n- [Home](index.md)\n"
                "## Quickstart {expanded=true}\n  - [Guide](guide.md)\n"
            )
            (docs / "layout.md").write_text(outline, encoding="utf-8")
            result = build_site(root=root, output=root / "site", release="preview")
            self.assertEqual(2, result.page_count)
            self.assertFalse((root / "site" / "layout" / "index.html").exists())
            messages = _init(root)
            self.assertFalse((docs / "layout.json").exists())
            self.assertEqual(outline, (docs / "layout.md").read_text(encoding="utf-8"))
            self.assertTrue(any("docs/layout.md" in message for message in messages))

    def test_escaped_titles_and_paths_with_spaces(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = self.make_project(root)
            (docs / "space name.md").write_text("# Spaced", encoding="utf-8")
            (docs / "layout.md").write_text(
                "Layout-Version: 1\nHome: index.md\nUnlisted: exclude\n"
                "# Start\n- [Home](index.md)\n- [One \\] two](<space name.md>)\n",
                encoding="utf-8",
            )
            config = load_config(root)
            self.assertEqual("One ] two", config.pages[1].title)
            self.assertEqual("space name.md", config.pages[1].path)

    def test_layout_file_cannot_be_published_as_a_page(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = self.make_project(root)
            (docs / "layout.md").write_text(
                "Layout-Version: 1\n# Start\n- [Home](index.md)\n- [Layout](layout.md)\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(DocSproutError, r"layout\.md:4:.*cannot be a navigation page"):
                load_config(root)

    def test_missing_page_and_empty_group_name_the_outline_line(self) -> None:
        for outline, expected in (
            ("# Start\n- [Missing](missing.md)\n", r"layout\.md:3:.*does not exist"),
            ("# Start\n## Empty\n", r"layout\.md:3:.*needs pages"),
        ):
            with self.subTest(outline=outline), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                docs = self.make_project(root)
                (docs / "layout.md").write_text(
                    "Layout-Version: 1\n" + outline, encoding="utf-8",
                )
                with self.assertRaisesRegex(DocSproutError, expected):
                    load_config(root)

    def test_unlisted_error_ignores_the_layout_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = self.make_project(root)
            (docs / "guide.md").unlink()
            (docs / "layout.md").write_text(
                "Layout-Version: 1\nUnlisted: error\n# Start\n- [Home](index.md)\n",
                encoding="utf-8",
            )
            self.assertEqual((), load_config(root).excluded_documents)

    def test_invalid_metadata_names_its_line(self) -> None:
        for field, message in (("Unlisted: maybe", "Unlisted must be"), ("Home: ../other.md", "invalid Markdown path")):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                docs = self.make_project(root)
                (docs / "layout.md").write_text(
                    f"Layout-Version: 1\n{field}\n# Start\n- [Home](index.md)\n", encoding="utf-8",
                )
                with self.assertRaisesRegex(DocSproutError, rf"layout\.md:2:.*{message}"):
                    load_config(root)

    def test_section_page_can_follow_a_group(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = self.make_project(root)
            (docs / "layout.md").write_text(
                "Layout-Version: 1\nHome: index.md\nUnlisted: exclude\n"
                "# Start\n## Quickstart {expanded=true}\n  - [Guide](guide.md)\n"
                "- [Overview](index.md)\n",
                encoding="utf-8",
            )
            config = load_config(root)
            self.assertEqual(("guide.md", "index.md"), tuple(page.path for page in config.pages))
            self.assertIsNone(config.pages[1].subsection)


if __name__ == "__main__":
    unittest.main()
