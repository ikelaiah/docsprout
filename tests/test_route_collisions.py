import json
from pathlib import Path
import tempfile
import unittest

from docsprout.build import build_site, detect_route_collisions
from docsprout.errors import DocSproutError
from docsprout.models import Page


class RouteCollisionTests(unittest.TestCase):
    def _project(
        self, root: Path, *, pages: list[dict], home: dict | None = None,
    ) -> None:
        docs = root / "docs"
        docs.mkdir()
        layout = {"schema_version": 1, "unlisted": "exclude", "navigation": [{"title": "Docs", "pages": pages}]}
        if home is not None:
            layout["home"] = home
        for page in pages:
            if page.get("source") == "root":
                (root / "README.md").write_text("# Root README", encoding="utf-8")
            else:
                path = root / "docs" / page["path"]
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"# {page['title']}", encoding="utf-8")
        (docs / "docsprout.json").write_text(json.dumps({"schema_version": 1, "project": {"name": "Demo"}}), encoding="utf-8")
        (docs / "layout.json").write_text(json.dumps(layout), encoding="utf-8")

    def test_detects_the_alternative_home_index_docs_index_collision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root, pages=[
                {"title": "Index", "path": "index.md"},
                {"title": "Docs index", "path": "docs-index.md"},
            ], home={"path": "guide.md"})
            (root / "docs" / "guide.md").write_text("# Guide", encoding="utf-8")
            (root / "docs" / "layout.json").write_text(json.dumps({
                "schema_version": 1, "unlisted": "exclude", "home": {"path": "guide.md"},
                "navigation": [{"title": "Docs", "pages": [
                    {"title": "Index", "path": "index.md"},
                    {"title": "Docs index", "path": "docs-index.md"},
                    {"title": "Guide", "path": "guide.md"},
                ]}],
            }), encoding="utf-8")

            with self.assertRaisesRegex(DocSproutError, r"Generated route collision: 'docs-index.html'.*'index\.md'.*'docs-index\.md'"):
                build_site(root=root, output=root / "site", release="dev")

    def test_detects_a_root_readme_and_docs_readme_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root, pages=[
                {"title": "Overview", "path": "README.md", "source": "root"},
                {"title": "Readme copy", "path": "README.md"},
            ])

            with self.assertRaisesRegex(DocSproutError, r"navigation page 'README\.md'.*appears more than once"):
                build_site(root=root, output=root / "site", release="dev")

    def test_detects_case_insensitive_route_collisions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root, pages=[
                {"title": "Foo", "path": "foo.md"},
                {"title": "Foo variant", "path": "Foo.md"},
                {"title": "Guide", "path": "guide.md"},
            ], home={"path": "guide.md"})

            with self.assertRaisesRegex(DocSproutError, r"Generated route collision"):
                build_site(root=root, output=root / "site", release="dev")

    def test_route_collision_detection_is_available_without_a_build(self) -> None:
        pages = (
            Page("index.md", "Index"),
            Page("docs-index.md", "Docs index"),
        )
        with self.assertRaisesRegex(DocSproutError, r"docs-index\.html"):
            detect_route_collisions(pages, "guide.md")

    def test_valid_routes_still_build_with_the_established_shapes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._project(root, pages=[
                {"title": "Index", "path": "index.md"},
                {"title": "Quick start", "path": "guides/quick-start.md"},
            ])

            build_site(root=root, output=root / "site", release="dev")

            self.assertTrue((root / "site" / "index.html").is_file())
            self.assertTrue((root / "site" / "guides" / "quick-start.html").is_file())