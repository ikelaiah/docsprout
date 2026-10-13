"""Reading-page navigation and responsive outline contracts."""

import json
from pathlib import Path
import tempfile
import unittest

from docsprout.build import build_site


class ReadingLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory()
        root = Path(cls.temporary.name)
        docs = root / "docs"
        docs.mkdir()
        sources = {
            "index.md": "# Welcome\n\nStart here.",
            "plain.md": "# Plain page\n\nA short page without sections.",
            "one.md": "# One section\n\n## Install\n\nRun the installer.",
            "long.md": "# Long guide\n\n## Prepare\n\nText.\n\n### Check\n\nText.\n\n## Finish\n\nText.",
        }
        for name, content in sources.items():
            (docs / name).write_text(content, encoding="utf-8")
        (docs / "docsprout.json").write_text(
            json.dumps({"schema_version": 1, "project": {"name": "Reading layout"}}), encoding="utf-8"
        )
        (docs / "layout.json").write_text(json.dumps({
            "schema_version": 1,
            "navigation": [
                {"title": "Start here", "pages": [{"title": "Welcome", "path": "index.md"}]},
                {"title": "Guides & use", "pages": [{"title": "Quickstart", "pages": [
                    {"title": "Plain page", "path": "plain.md"},
                    {"title": "One section", "path": "one.md"},
                ]}]},
                {"title": "Reference", "pages": [{"title": "Long guide", "path": "long.md"}]},
            ],
        }), encoding="utf-8")
        output = root / "site"
        build_site(root=root, output=output, release="test")
        cls.pages = {name: (output / name).read_text(encoding="utf-8") for name in (
            "index.html", "plain.html", "one.html", "long.html"
        )}
        cls.css = (output / "assets" / "site.css").read_text(encoding="utf-8")
        cls.js = (output / "assets" / "site.js").read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def test_context_precedes_reading_title_and_homepage_is_unchanged(self) -> None:
        plain = self.pages["plain.html"]
        self.assertIn('<nav class="page-context" aria-label="Breadcrumb"><ol>', plain)
        self.assertIn("<li><span>Guides &amp; use</span></li>", plain)
        self.assertIn("<li><span>Quickstart</span></li>", plain)
        self.assertLess(plain.index('class="page-context"'), plain.index('<h1 id="plain-page">'))
        self.assertNotIn('class="page-context"', self.pages["index.html"])
        self.assertNotIn('class="inline-toc"', self.pages["index.html"])
        self.assertNotIn('class="page-nav-context"', self.pages["index.html"])
        self.assertIn('<small>Next</small><span>Plain page</span>', self.pages["index.html"])

    def test_reading_page_without_sections_has_no_empty_outline_column(self) -> None:
        plain = self.pages["plain.html"]
        self.assertIn('<div class="shell shell-no-toc">', plain)
        self.assertNotIn('<aside class="toc"', plain)
        self.assertNotIn('class="inline-toc"', plain)
        self.assertIn('.shell-no-toc{', self.css)

    def test_single_and_nested_sections_have_disclosure_after_title(self) -> None:
        for route, fragments in (("one.html", ("install",)), ("long.html", ("prepare", "check", "finish"))):
            with self.subTest(route=route):
                page = self.pages[route]
                self.assertIn('<details class="inline-toc"><summary>On this page</summary>', page)
                self.assertIn('<nav aria-label="Page outline">', page)
                self.assertIn('<aside class="toc" aria-label="On this page">', page)
                main = page[page.index('<main class="prose"'):page.index('</main>')]
                self.assertLess(main.index('</h1>'), main.index('class="inline-toc"'))
                self.assertLess(main.index('class="inline-toc"'), main.index('<h2'))
                for fragment in fragments:
                    self.assertEqual(2, page.count(f'href="#{fragment}"'))
                self.assertIn('<div class="shell">', page)
        self.assertIn('.inline-toc{display:none}', self.css)
        self.assertIn('@media(max-width:1024px)', self.css)
        self.assertIn('.inline-toc{display:block', self.css)

    def test_previous_and_next_show_destination_context(self) -> None:
        plain = self.pages["plain.html"]
        self.assertIn('<small>Previous</small><span class="page-nav-context">Start here</span><span>Welcome</span>', plain)
        self.assertIn('<small>Next</small><span class="page-nav-context">Guides &amp; use / Quickstart</span><span>One section</span>', plain)
        one = self.pages["one.html"]
        self.assertIn('<small>Next</small><span class="page-nav-context">Reference</span><span>Long guide</span>', one)

    def test_scroll_tracking_does_not_open_the_readers_outline(self) -> None:
        self.assertNotRegex(self.js, r"\.open\s*=\s*true")
        self.assertIn("'aria-current'", self.js)

    def test_phone_header_and_progress_follow_the_reading_article(self) -> None:
        page = self.pages["long.html"]
        self.assertIn('<main class="prose" id="content"', page)
        self.assertIn('.site-header.is-compact .brand:not(:focus){position:absolute', self.css)
        self.assertIn("document.querySelector('main.prose')", self.js)
        self.assertIn("header.classList.toggle('is-compact'", self.js)
        self.assertNotIn('document.documentElement.scrollHeight-window.innerHeight', self.js)


if __name__ == "__main__":
    unittest.main()
