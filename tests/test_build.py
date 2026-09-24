import json
from pathlib import Path
import tempfile
import unittest

from docsprout.build import build_site
from docsprout.errors import DocSproutError


class BuildSiteTests(unittest.TestCase):
    def test_publishes_local_markdown_images_with_their_page(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            (docs / "images").mkdir(parents=True)
            (docs / "index.md").write_text("# Home\n\n![Architecture](images/architecture.svg)\n", encoding="utf-8")
            (docs / "images" / "architecture.svg").write_text("<svg/>", encoding="utf-8")
            (docs / "docsprout.json").write_text(json.dumps({"schema_version": 1, "project": {"name": "Demo"}}), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({
                "schema_version": 1,
                "navigation": [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}]}],
            }), encoding="utf-8")

            build_site(root=root, output=root / "site", release="dev")

            page = (root / "site" / "index.html").read_text(encoding="utf-8")
            self.assertIn('<img src="assets/content/images/architecture.svg" alt="Architecture">', page)
            self.assertEqual("<svg/>", (root / "site" / "assets" / "content" / "images" / "architecture.svg").read_text(encoding="utf-8"))

    def test_publishes_nested_page_assets_under_a_non_colliding_content_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            (docs / "guides").mkdir(parents=True)
            (docs / "images").mkdir()
            (docs / "assets").mkdir()
            (docs / "index.md").write_text("# Home\n", encoding="utf-8")
            (docs / "guides" / "advanced.md").write_text(
                "# Advanced\n\n![Diagram](../images/diagram.svg)\n![Theme](../assets/site.css)\n", encoding="utf-8"
            )
            (docs / "images" / "diagram.svg").write_text("<svg/>", encoding="utf-8")
            (docs / "assets" / "site.css").write_text("documentation asset", encoding="utf-8")
            (docs / "docsprout.json").write_text(json.dumps({"schema_version": 1, "project": {"name": "Demo"}}), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({
                "schema_version": 1,
                "navigation": [{"title": "Docs", "pages": [
                    {"title": "Home", "path": "index.md"},
                    {"title": "Advanced", "path": "guides/advanced.md"},
                ]}],
            }), encoding="utf-8")

            build_site(root=root, output=root / "site", release="dev")

            page = (root / "site" / "guides" / "advanced.html").read_text(encoding="utf-8")
            self.assertIn('<img src="../assets/content/images/diagram.svg" alt="Diagram">', page)
            self.assertIn('<img src="../assets/content/assets/site.css" alt="Theme">', page)
            self.assertEqual("documentation asset", (root / "site" / "assets" / "content" / "assets" / "site.css").read_text(encoding="utf-8"))
            self.assertNotEqual("documentation asset", (root / "site" / "assets" / "site.css").read_text(encoding="utf-8"))

    def test_refuses_markdown_assets_that_escape_docs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (root / "outside.svg").write_text("<svg/>", encoding="utf-8")
            (docs / "index.md").write_text("# Home\n\n![Outside](../outside.svg)\n", encoding="utf-8")
            (docs / "docsprout.json").write_text(json.dumps({"schema_version": 1, "project": {"name": "Demo"}}), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({
                "schema_version": 1,
                "navigation": [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}]}],
            }), encoding="utf-8")

            with self.assertRaisesRegex(DocSproutError, "unsafe local link"):
                build_site(root=root, output=root / "site", release="dev")

    def test_builds_the_maintained_minimal_example(self) -> None:
        root = Path(__file__).resolve().parents[1] / "examples" / "minimal"
        with tempfile.TemporaryDirectory() as temporary:
            result = build_site(root=root, output=Path(temporary) / "site", release="example")

            self.assertEqual(2, result.page_count)
            page = (Path(temporary) / "site" / "quick-start.html").read_text(encoding="utf-8")
            self.assertIn("Change the accent colours", page)
            self.assertIn('data-content-width="compact"', page)

    def test_builds_the_maintained_visual_fixture(self) -> None:
        root = Path(__file__).resolve().parents[1] / "examples" / "visual-fixtures"
        with tempfile.TemporaryDirectory() as temporary:
            result = build_site(root=root, output=Path(temporary) / "site", release="fixture")

            self.assertEqual(2, result.page_count)
            home = (Path(temporary) / "site" / "index.html").read_text(encoding="utf-8")
            long_form = (Path(temporary) / "site" / "long-form.html").read_text(encoding="utf-8")
            self.assertIn('data-content-width="wide"', home)
            self.assertIn('class="admonition important"', home)
            self.assertIn('class="table-scroll"', home)
            self.assertIn("Long-form reading fixture", long_form)
            self.assertTrue((Path(temporary) / "site" / "assets" / "banner.svg").is_file())
            self.assertIn('class="banner" src="assets/banner.svg"', home)
            self.assertIn('<div class="hero hero-art"><div class="hero-figure"><img class="banner"', home)
            self.assertIn('</div><div class="hero-copy">', home)
            custom_css = Path(temporary) / "site" / "assets" / "custom.css"
            self.assertTrue(custom_css.is_file())
            self.assertIn("var(--dk-accent)", custom_css.read_text(encoding="utf-8"))
            self.assertIn('href="assets/custom.css"', home)
            self.assertGreater(
                home.index('href="assets/custom.css"'),
                home.index('href="assets/site.css"'),
            )

    def test_copies_an_identity_logo_into_the_header(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            (docs / "assets").mkdir(parents=True)
            (docs / "index.md").write_text("# Home", encoding="utf-8")
            (docs / "assets" / "logo.svg").write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 8 8"/>', encoding="utf-8"
            )
            (docs / "docsprout.json").write_text(json.dumps({
                "schema_version": 1,
                "project": {"name": "Logo Demo"},
                "identity": {"logo": "docs/assets/logo.svg"},
            }), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({
                "schema_version": 1,
                "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}],
            }), encoding="utf-8")

            build_site(root=root, output=root / "site", release="dev")

            home = (root / "site" / "index.html").read_text(encoding="utf-8")
            self.assertTrue((root / "site" / "assets" / "logo.svg").is_file())
            self.assertIn('class="brand-logo" src="assets/logo.svg" alt="" aria-hidden="true"', home)
            self.assertNotIn('class="brand-mark"', home)

    def test_builds_modern_navigation_search_and_theme_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            (docs / "guides").mkdir(parents=True)
            (docs / "index.md").write_text(
                "# Welcome\n\nA **safe** start with $x^2$.\n\n## Quick start\n\nBegin here.",
                encoding="utf-8",
            )
            (docs / "guides" / "pascal.md").write_text(
                "# Pascal\n\n```pascal\nWriteLn('hello');\n```", encoding="utf-8"
            )
            (docs / "docsprout.json").write_text(json.dumps({
                "schema_version": 1,
                "project": {"name": "Demo-FP", "description": "Demo docs", "repository_url": "https://example.test/demo"},
                "theme": {"accent": "#0f766e", "accent_secondary": "#0891b2"},
                "identity": {"footer": "Demo footer", "links": [{"label": "Repository", "url": "https://example.test/demo"}]},
            }), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({
                "schema_version": 1,
                "navigation": [{"title": "Start", "pages": [
                    {"title": "Welcome", "path": "index.md"},
                    {"title": "Pascal", "path": "guides/pascal.md"},
                ]}],
            }), encoding="utf-8")

            result = build_site(root=root, output=root / "site", release="dev")

            self.assertEqual(2, result.page_count)
            home = (root / "site" / "index.html").read_text(encoding="utf-8")
            self.assertIn('style="--dk-accent:#0f766e;--dk-accent-secondary:#0891b2"', home)
            self.assertIn('id="visual-theme"', home)
            self.assertIn('data-visual-theme="classic"', home)
            self.assertIn('data-content-width="comfortable"', home)
            self.assertIn('<link rel="icon" href="data:image/svg+xml,', home)
            self.assertIn("System", home)
            self.assertIn("search-index.json", home)
            self.assertIn('placeholder="Search docs, commands, and versions"', home)
            self.assertIn('class="brand-mark"', home)
            self.assertIn('class="capability-strip"', home)
            self.assertIn('data-card-count="4"', home)
            self.assertIn('data-homepage="true"', home)
            self.assertIn("<script>try{const root=document.documentElement,readStored=(primary,legacy)=>{const value=localStorage.getItem(primary);if(value!==null)return value;const previous=localStorage.getItem(legacy);", home)
            self.assertLess(
                home.index("readStored('docsprout-visual-theme','dockit-fp-visual-theme')"),
                home.index('<link rel="stylesheet" href="assets/site.css">'),
            )
            self.assertIn('class="header-controls"', home)
            self.assertIn('aria-current="page"', home)
            self.assertIn('aria-label="Demo-FP capabilities"', home)
            self.assertIn('class="reading-progress"', home)
            self.assertNotIn('class="release-lens"', home)
            self.assertNotIn('<dt>Release</dt>', home)
            self.assertIn('class="page-navigation"', home)
            self.assertIn('class="site-footer"', home)
            self.assertIn('href="https://example.test/demo"', home)
            self.assertIn('class="page-next"', home)
            self.assertIn('<span>Pascal</span>', home)
            self.assertGreater(home.index('class="capability-strip"'), home.index('A <strong>safe</strong> start'))
            self.assertIn('aria-controls="search-results"', home)
            self.assertIn('aria-describedby="search-help"', home)
            self.assertIn('id="search-help"', home)
            self.assertIn('href="#quick-start"', home)
            self.assertIn("assets/katex/katex.min.css", home)
            self.assertIn('class="math-inline" data-tex="x^2"', home)
            self.assertTrue((root / "site" / "assets" / "katex" / "katex.min.js").exists())
            self.assertTrue((root / "site" / "assets" / "katex" / "LICENSE").exists())
            self.assertTrue((root / "site" / "guides" / "pascal.html").exists())
            pascal = (root / "site" / "guides" / "pascal.html").read_text(encoding="utf-8")
            self.assertIn('class="page-previous" href="../index.html"', pascal)
            site_js = (root / "site" / "assets" / "site.js").read_text(encoding="utf-8")
            self.assertIn("copy-code", site_js)
            self.assertIn("ArrowDown", site_js)
            self.assertIn("function rank", site_js)
            self.assertIn("event.key==='Home'", site_js)
            self.assertIn("event.key==='End'", site_js)
            site_css = (root / "site" / "assets" / "site.css").read_text(encoding="utf-8")
            system_classic_dark_rule = (
                '@media(prefers-color-scheme:dark){html[data-visual-theme="classic"]'
                ':not([data-theme]){color-scheme:dark;--dk-bg:#111827;--dk-surface:#1f2937;'
                '--dk-text:#f3f4f6;--dk-muted:#b8c2d3;--dk-border:#3b4659;--dk-code-bg:#030712}}'
            )
            self.assertIn(
                system_classic_dark_rule,
                site_css,
            )
            self.assertIn(
                '@media(prefers-color-scheme:dark){html[data-visual-theme="classic"]'
                ':not([data-theme]){--dk-raised:#172033;--dk-focus-ring:#67e8f9;'
                '--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}}',
                site_css,
            )
            self.assertIn('--dk-content-width:46rem', site_css)
            self.assertIn('--dk-interactive:color-mix(in srgb,var(--dk-accent) 78%,#000)', site_css)
            self.assertIn('--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)', site_css)
            self.assertIn('html[data-content-width="wide"]{--dk-content-width:54rem', site_css)
            self.assertIn('--dk-space-1:.25rem', site_css)
            self.assertIn('--dk-control-height:2.5rem', site_css)
            self.assertIn('.capability-strip[data-card-count="3"]', site_css)
            self.assertIn('align-items:stretch;grid-template-rows:minmax(0,1fr)', site_css)
            self.assertIn('.capability-strip li{display:flex;flex-direction:column;align-self:stretch;min-height:0;padding:1.1rem 1.15rem;border:1px solid var(--dk-border);border-radius:.55rem', site_css)
            self.assertIn('.capability-strip li+li{margin-top:0}', site_css)
            self.assertIn('.header-controls', site_css)
            self.assertIn('.topbar{display:grid;grid-template-columns:auto minmax(12rem,30rem) max-content;grid-template-rows:auto var(--dk-control-height)', site_css)
            self.assertIn('.page-navigation a{min-height:0;max-width:none;padding:0;border:0;border-radius:0;background:transparent', site_css)
            self.assertIn('.page-navigation .page-next{grid-column:1;justify-self:start}', site_css)
            self.assertIn('.hero .hero-copy>p', site_css)
            self.assertIn('.hero-copy{min-width:0}', site_css)
            self.assertIn('.hero.hero-art{display:flex;flex-direction:column;padding:0}', site_css)
            self.assertIn(
                '.prose .hero-primary{border:1px solid color-mix(in srgb,var(--dk-interactive) 72%,#000);'
                'background:var(--dk-interactive);color:var(--dk-on-interactive,#fff)}',
                site_css,
            )
            self.assertIn('.prose h1,.prose h2,.prose h3{font-family:var(--dk-font-display);font-weight:720;letter-spacing:-.032em;text-wrap:balance}', site_css)
            self.assertIn('.prose h1{max-width:none;margin-bottom:1.25rem}', site_css)
            self.assertIn('@media(prefers-reduced-motion:reduce)', site_css)
            self.assertIn('.syntax-highlight .tok-property{color:#93c5fd}', site_css)
            self.assertIn('.syntax-highlight .tok-keyword{color:#c4b5fd}', site_css)
            self.assertIn(
                '@media(max-width:600px){.topbar{gap:.5rem}.brand{flex:0 0 100%}'
                '.topbar select{flex:0 1 calc(50% - .25rem);width:calc(50% - .25rem);min-width:0}'
                '.capability-strip{grid-template-columns:1fr}}',
                site_css,
            )
            search = json.loads((root / "site" / "search-index.json").read_text(encoding="utf-8"))
            self.assertEqual(1, search["schema_version"])
            self.assertEqual(["index.html", "guides/pascal.html"], [entry["url"] for entry in search["entries"]])

    def test_home_page_renders_a_splash_hero_with_derived_actions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Welcome\n\nA short introduction.\n\n## Next\n\nMore.", encoding="utf-8")
            (docs / "guide.md").write_text("# Guide", encoding="utf-8")
            (docs / "docsprout.json").write_text(json.dumps({
                "schema_version": 1,
                "project": {"name": "Hero Demo", "repository_url": "https://example.test/hero"},
                "homepage": {"sections": {"release_context": True}},
            }), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({"schema_version": 1, "navigation": [{"title": "Start", "pages": [
                {"title": "Welcome", "path": "index.md"}, {"title": "Guide", "path": "guide.md"},
            ]}]}), encoding="utf-8")

            build_site(root=root, output=root / "site", release="1.1.4")

            home = (root / "site" / "index.html").read_text(encoding="utf-8")
            guide = (root / "site" / "guide.html").read_text(encoding="utf-8")
            self.assertIn('<div class="hero"><div class="hero-copy">', home)
            hero_copy = home[home.index('class="hero-copy"'):home.index('class="hero-actions"')]
            self.assertIn("<h1", hero_copy)
            self.assertIn("A short introduction.", hero_copy)
            self.assertIn('class="release-context"', hero_copy)
            self.assertIn('<a class="hero-primary" href="guide.html">Get started</a>', home)
            self.assertIn('<a class="hero-secondary" href="https://example.test/hero">Repository</a>', home)
            self.assertIn('<style>:root{--dk-interactive:', home)
            self.assertIn("--dk-on-interactive:", home)
            self.assertIn("prefers-color-scheme:dark", home)
            self.assertEqual(4, home.count('class="card-icon"'))
            self.assertIn('<svg class="card-icon" viewBox="0 0 24 24" aria-hidden="true"', home)
            self.assertGreater(home.index('class="capability-strip"'), home.index('class="hero-actions"'))
            self.assertNotIn('<div class="hero', guide)
            self.assertNotIn("hero-actions", guide)

    def test_home_page_omits_a_repository_action_without_a_safe_url(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Welcome\n", encoding="utf-8")
            (docs / "docsprout.json").write_text(json.dumps({
                "schema_version": 1,
                "project": {"name": "Hero Demo", "repository_url": "javascript:alert(1)"},
            }), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({"schema_version": 1, "navigation": [
                {"title": "Start", "pages": [{"title": "Welcome", "path": "index.md"}]},
            ]}), encoding="utf-8")

            build_site(root=root, output=root / "site", release="dev")

            home = (root / "site" / "index.html").read_text(encoding="utf-8")
            self.assertNotIn("javascript:", home)
            self.assertNotIn("hero-actions", home)
            self.assertNotIn("hero-secondary", home)

    def test_marks_a_custom_three_card_homepage_for_responsive_layout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Home\n\nA short introduction.", encoding="utf-8")
            (docs / "docsprout.json").write_text(json.dumps({
                "schema_version": 1,
                "project": {"name": "Three Cards"},
                "homepage": {"capabilities": [
                    {"title": "One", "description": "First"},
                    {"title": "Two", "description": "Second"},
                    {"title": "Three", "description": "Third"},
                ]},
            }), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({
                "schema_version": 1,
                "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}],
            }), encoding="utf-8")

            build_site(root=root, output=root / "site", release="dev")

            home = (root / "site" / "index.html").read_text(encoding="utf-8")
            self.assertIn('class="capability-strip" data-card-count="3"', home)
            self.assertIn('aria-label="Three Cards capabilities"', home)
            self.assertIn('class="header-controls"', home)
            self.assertIn('data-homepage="true"', home)

    def test_uses_readme_as_home_for_configuration_free_legacy_docs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "README.md").write_text("# Old documentation\n\nThe original home.", encoding="utf-8")
            (docs / "CHEATSHEET.md").write_text("# Cheat sheet", encoding="utf-8")

            result = build_site(root=root, output=root / "site", release="1.0.0")

            self.assertTrue(result.legacy)
            self.assertEqual("README.md", result.home_document)
            self.assertIn("Old documentation", (root / "site" / "index.html").read_text(encoding="utf-8"))
            self.assertTrue((root / "site" / "CHEATSHEET.html").exists())

    def test_builds_an_explicit_repository_root_readme_without_copying_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            readme = root / "README.md"
            readme.write_text("# Root documentation\n\n[Guide](docs/guide.md)", encoding="utf-8")
            (docs / "guide.md").write_text("# Guide\n\n[Back](../README.md)", encoding="utf-8")
            (docs / "docsprout.json").write_text(json.dumps({"schema_version": 1, "project": {"name": "Demo"}}), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({"schema_version": 1, "navigation": [
                {"title": "Overview", "pages": [{"title": "Overview", "path": "README.md", "source": "root"}]},
                {"title": "Guides", "pages": [{"title": "Guide", "path": "guide.md"}]},
            ]}), encoding="utf-8")

            build_site(root=root, output=root / "site", release="dev")

            self.assertIn('href="guide.html"', (root / "site" / "index.html").read_text(encoding="utf-8"))
            self.assertIn('href="index.html"', (root / "site" / "guide.html").read_text(encoding="utf-8"))
            self.assertEqual("# Root documentation\n\n[Guide](docs/guide.md)", readme.read_text(encoding="utf-8"))

    def test_keeps_docs_index_reachable_when_another_page_is_the_explicit_home(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Documentation index", encoding="utf-8")
            (docs / "guide.md").write_text("# Getting started", encoding="utf-8")
            (docs / "docsprout.json").write_text(json.dumps({"schema_version": 1, "project": {"name": "Demo"}}), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({"schema_version": 1, "home": {"path": "guide.md"}, "navigation": [{"title": "Docs", "pages": [
                {"title": "Index", "path": "index.md"}, {"title": "Guide", "path": "guide.md"},
            ]}]}), encoding="utf-8")

            build_site(root=root, output=root / "site", release="dev")

            self.assertIn("Getting started", (root / "site" / "index.html").read_text(encoding="utf-8"))
            self.assertIn("Documentation index", (root / "site" / "docs-index.html").read_text(encoding="utf-8"))

    def test_excludes_unlisted_markdown_when_layout_requests_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Home", encoding="utf-8")
            (docs / "guide.md").write_text("# Guide", encoding="utf-8")
            (docs / "private.md").write_text("# Private", encoding="utf-8")
            (docs / "docsprout.json").write_text(json.dumps({"schema_version": 1, "project": {"name": "Demo"}}), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({"schema_version": 1, "unlisted": "exclude", "navigation": [{"title": "Docs", "pages": [
                {"title": "Home", "path": "index.md"}, {"title": "Guide", "path": "guide.md"},
            ]}]}), encoding="utf-8")

            result = build_site(root=root, output=root / "site", release="dev")

            self.assertEqual(2, result.page_count)
            self.assertEqual(1, result.excluded_count)
            self.assertTrue((root / "site" / "guide.html").is_file())
            self.assertFalse((root / "site" / "private.html").exists())

    def test_root_readme_remains_the_home_when_docs_contains_index(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (root / "README.md").write_text("# Repository overview", encoding="utf-8")
            (docs / "index.md").write_text("# Docs overview", encoding="utf-8")
            (docs / "docsprout.json").write_text(json.dumps({"schema_version": 1, "project": {"name": "Demo"}}), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({"schema_version": 1, "navigation": [
                {"title": "Overview", "pages": [{"title": "Repository", "path": "README.md", "source": "root"}]},
                {"title": "Documentation", "pages": [{"title": "Docs", "path": "index.md"}]},
            ]}), encoding="utf-8")

            build_site(root=root, output=root / "site", release="dev")

            self.assertIn("Repository overview", (root / "site" / "index.html").read_text(encoding="utf-8"))
            self.assertIn("Docs overview", (root / "site" / "docs-index.html").read_text(encoding="utf-8"))

    def test_places_home_capabilities_outside_an_initial_admonition(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Home\n\n> [!IMPORTANT] Read this first.\n\nWelcome.", encoding="utf-8")

            build_site(root=root, output=root / "site", release="dev")

            page = (root / "site" / "index.html").read_text(encoding="utf-8")
            callout_start = page.index('<aside class="admonition')
            callout_end = page.index("</aside>", callout_start)
            strip_start = page.index('class="capability-strip"')
            self.assertFalse(callout_start < strip_start < callout_end)

    def test_configures_homepage_content_without_changing_other_pages(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Home\n\nWelcome to <safe> docs.\n\n## Details\n\nKeep this content.", encoding="utf-8")
            (docs / "guide.md").write_text("# Guide\n\nWelcome to the guide.", encoding="utf-8")
            (docs / "docsprout.json").write_text(json.dumps({
                "schema_version": 1,
                "project": {"name": "Demo"},
                "homepage": {
                    "capabilities": [{"title": "<Fast>", "description": "Use <safe> local assets."}],
                    "sections": {"introduction": False, "release_context": True},
                },
            }), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({"schema_version": 1, "navigation": [{"title": "Start", "pages": [
                {"title": "Home", "path": "index.md"}, {"title": "Guide", "path": "guide.md"},
            ]}]}), encoding="utf-8")

            build_site(root=root, output=root / "site", release="0.6.0")

            home = (root / "site" / "index.html").read_text(encoding="utf-8")
            guide = (root / "site" / "guide.html").read_text(encoding="utf-8")
            self.assertIn("&lt;Fast&gt;", home)
            self.assertIn("Use &lt;safe&gt; local assets.", home)
            self.assertNotIn("<p>Welcome to &lt;safe&gt; docs.</p>", home)
            self.assertIn('class="release-context"', home)
            self.assertIn("0.6.0", home)
            self.assertNotIn('class="capability-strip"', guide)
            self.assertNotIn('class="release-context"', guide)

    def test_typography_layer_is_cross_platform_complete_and_print_ready(self) -> None:
        root = Path(__file__).resolve().parents[1] / "examples" / "visual-fixtures"
        with tempfile.TemporaryDirectory() as temporary:
            build_site(root=root, output=Path(temporary) / "site", release="fixture")

            css = (Path(temporary) / "site" / "assets" / "site.css").read_text(encoding="utf-8")
            self.assertIn('--dk-font-ui:system-ui,-apple-system,"Segoe UI",Inter,"Aptos",sans-serif', css)
            self.assertIn('--dk-font-mono:ui-monospace,SFMono-Regular,Menlo,Consolas,"Cascadia Code",monospace', css)
            for selector in (".prose h4{", ".prose h5{", ".prose h6{", ".toc .toc-level-4{", ".toc .toc-level-5{", ".toc .toc-level-6{"):
                with self.subTest(selector=selector):
                    self.assertIn(selector, css)
            self.assertIn("text-wrap:pretty;orphans:3;widows:3", css)
            self.assertIn("hyphens:auto", css)
            self.assertIn("font-variant-numeric:tabular-nums", css)
            self.assertIn("::selection", css)
            self.assertIn("@media print{", css)
            self.assertIn(".prose p,.prose li{hyphens:none}", css)

            home = (Path(temporary) / "site" / "index.html").read_text(encoding="utf-8")
            for identifier in ("heading-level-four", "heading-level-five", "heading-level-six"):
                with self.subTest(identifier=identifier):
                    self.assertIn(f'id="{identifier}"', home)
            self.assertIn('class="toc-level-4" href="#heading-level-four"', home)
            self.assertIn("don’t", home)
            self.assertIn("—", home)
            self.assertIn("…", home)
            self.assertIn("<code>--flag</code>", home)
            self.assertIn("<code>don't</code>", home)

    def test_rejects_broken_heading_fragments_and_unsafe_links(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "README.md").write_text("# Old\n\n[Broken](other.md#absent)", encoding="utf-8")
            (docs / "other.md").write_text("# Present", encoding="utf-8")

            with self.assertRaisesRegex(DocSproutError, "heading fragment"):
                build_site(root=root, output=root / "site", release="1.0.0")

            (docs / "README.md").write_text("# Old\n\n[Unsafe](javascript:alert(1))", encoding="utf-8")
            with self.assertRaisesRegex(DocSproutError, "unsafe URL"):
                build_site(root=root, output=root / "site", release="1.0.0")

    def test_escapes_configuration_values_in_the_html_shell(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Safe", encoding="utf-8")
            (docs / "docsprout.json").write_text(json.dumps({
                "schema_version": 1, "project": {"name": "<script>x</script>", "description": "\" onload=alert(1)"},
            }), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({"schema_version": 1, "navigation": [{"title": "<bad>", "pages": [{"title": "<bad>", "path": "index.md"}]}]}), encoding="utf-8")

            build_site(root=root, output=root / "site", release="dev")

            page = (root / "site" / "index.html").read_text(encoding="utf-8")
            self.assertNotIn("<script>x</script>", page)
            self.assertIn("&lt;script&gt;x&lt;/script&gt;", page)
