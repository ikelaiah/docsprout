import json
from pathlib import Path
import unittest

from dockit_fp import __version__


class DocumentationUsabilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parents[1]

    def test_readme_keeps_one_short_path_to_a_local_preview(self) -> None:
        readme = (self.root / "README.md").read_text(encoding="utf-8")

        self.assertLessEqual(len(readme.splitlines()), 150)
        self.assertEqual(1, sum(line.startswith("# ") for line in readme.splitlines()))
        self.assertIn("first site in about 10 minutes", readme)
        self.assertIn("You can stop here", readme)
        self.assertIn("dockit-fp/archive/refs/tags/v1.0.0.zip", readme)
        self.assertNotIn('pip install "dockit-fp==', readme)

    def test_readme_badges_are_canonical_and_deliberate(self) -> None:
        readme = (self.root / "README.md").read_text(encoding="utf-8")

        expected_badges = (
            "[![CI](https://github.com/ikelaiah/dockit-fp/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ikelaiah/dockit-fp/actions/workflows/ci.yml?query=branch%3Amain)",
            "[![Docs](https://img.shields.io/website?url=https%3A%2F%2Fikelaiah.github.io%2Fdockit-fp%2F1.0.0%2F&label=docs)](https://ikelaiah.github.io/dockit-fp/1.0.0/)",
            "[![Latest release](https://img.shields.io/github/v/release/ikelaiah/dockit-fp?display_name=tag&sort=semver)](https://github.com/ikelaiah/dockit-fp/releases/latest)",
            "[![Python 3.10–3.14](https://img.shields.io/badge/python-3.10%E2%80%933.14-3776AB?logo=python&logoColor=white)](https://github.com/ikelaiah/dockit-fp/blob/main/docs/qualification.md#supported-python-versions)",
            "[![License: MIT](https://img.shields.io/github/license/ikelaiah/dockit-fp)](https://github.com/ikelaiah/dockit-fp/blob/main/LICENSE)",
        )
        for badge in expected_badges:
            with self.subTest(badge=badge):
                self.assertIn(badge, readme)
        self.assertNotIn("python-3.10%2B", readme)

    def test_navigation_puts_learning_before_project_internals(self) -> None:
        layout = json.loads((self.root / "docs" / "layout.json").read_text(encoding="utf-8"))
        sections = layout["navigation"]

        self.assertEqual("Start here", sections[0]["title"])
        self.assertEqual(
            ["index.md", "beginners-guide.md", "writing-great-docs.md", "glossary.md"],
            [page["path"] for page in sections[0]["pages"]],
        )
        self.assertGreater(
            next(index for index, section in enumerate(sections) if section["title"] == "Pascal and project internals"),
            next(index for index, section in enumerate(sections) if section["title"] == "Publish safely"),
        )

    def test_recommended_layouts_use_the_explicit_modern_contract(self) -> None:
        layouts = {
            "DocKit": self.root / "docs" / "layout.json",
            "minimal example": self.root / "examples" / "minimal" / "docs" / "layout.json",
            "single-version example": self.root / "examples" / "single-version" / "docs" / "layout.json",
            "historical example": self.root / "examples" / "historical" / "docs" / "layout.json",
            "visual fixture": self.root / "examples" / "visual-fixtures" / "docs" / "layout.json",
            "audit fixture": self.root / "examples" / "audit-fixture" / "docs" / "layout.json",
        }

        for name, path in layouts.items():
            with self.subTest(name=name):
                layout = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual({"path": "index.md"}, layout["home"])
                self.assertEqual("exclude", layout["unlisted"])

    def test_release_metadata_and_version_manifest_agree(self) -> None:
        manifest = json.loads((self.root / "docs" / "versions.json").read_text(encoding="utf-8"))

        self.assertEqual("1.0.0", __version__)
        self.assertEqual(__version__, manifest["current"])
        self.assertEqual(f"v{__version__}", manifest["versions"][0]["source_ref"])

        pyproject = (self.root / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('version = "1.0.0"', pyproject)
        self.assertIn('Development Status :: 5 - Production/Stable', pyproject)

    def test_beginner_guide_shows_complete_docs_and_root_readme_layouts(self) -> None:
        beginner = (self.root / "docs" / "beginners-guide.md").read_text(encoding="utf-8")

        self.assertIn('"home": {\n    "path": "README.md",\n    "source": "root"\n  }', beginner)
        self.assertIn('"home": {\n  "path": "index.md"\n}', beginner)
        self.assertIn('"unlisted": "exclude"', beginner)

    def test_writing_guide_is_language_neutral_and_result_focused(self) -> None:
        guide = (self.root / "docs" / "writing-great-docs.md").read_text(encoding="utf-8")
        words = " ".join(guide.split())

        self.assertIn("Pascal, Python, JavaScript or something else", words)
        self.assertIn("This page helps **[person]** to **[result]**", guide)
        self.assertIn("Show what success looks like", guide)

    def test_beginner_add_page_guidance_preserves_the_existing_home_entry(self) -> None:
        beginner = (self.root / "docs" / "beginners-guide.md").read_text(encoding="utf-8")
        configuration = (self.root / "docs" / "configuration.md").read_text(encoding="utf-8")

        self.assertIn("Keep the existing `home` entry unchanged", beginner)
        self.assertIn("Before the change, the file may look like this", beginner)
        self.assertIn("After adding the page, the file may look like this", beginner)
        self.assertIn('"title": "Quick start",\n  "path": "quick-start.md"', beginner)
        self.assertIn('},\n        {\n          "title": "Quick start"', beginner)
        self.assertNotIn('{"title": "Overview", "path": "index.md"}', beginner)
        root_policy = "Only the repository-root `README.md` has special root-source support."
        self.assertIn(root_policy, beginner)
        self.assertIn(root_policy, configuration)

    def test_docs_project_demonstrates_its_homepage_configuration(self) -> None:
        config = json.loads((self.root / "docs" / "dockit.json").read_text(encoding="utf-8"))
        guide = (self.root / "docs" / "homepage-recipes.md").read_text(encoding="utf-8")

        self.assertEqual(
            [
                "Existing-project friendly",
                "Polished with little setup",
                "Versioned documentation",
                "Offline/local assets",
            ],
            [card["title"] for card in config["homepage"]["capabilities"]],
        )
        self.assertTrue(config["homepage"]["sections"]["release_context"])
        self.assertIn("The home page is the Markdown document selected by `layout.json.home`", guide)
        self.assertIn("## See it in DocKit", guide)

    def test_docs_project_dogfoods_its_identity_configuration(self) -> None:
        config = json.loads((self.root / "docs" / "dockit.json").read_text(encoding="utf-8"))
        customisation = (self.root / "docs" / "customisation.md").read_text(encoding="utf-8")

        self.assertEqual("purple", config["theme"]["preset"])
        self.assertEqual("docs/assets/dockit-mark.svg", config["identity"]["logo"])
        self.assertTrue((self.root / config["identity"]["logo"]).is_file())
        self.assertEqual("Built with DocKit.", config["identity"]["footer"])
        self.assertEqual(
            [{"label": "Project", "url": "https://github.com/ikelaiah/dockit-fp"}],
            config["identity"]["links"],
        )
        self.assertIn("### Before (default configuration)", customisation)
        self.assertIn("### After (DocKit's own configuration)", customisation)
        self.assertIn("blue colour preset", customisation)
        self.assertIn("no custom identity footer or link", customisation)

    def test_banner_guide_points_to_the_maintained_banner_fixture(self) -> None:
        config = json.loads(
            (self.root / "examples" / "visual-fixtures" / "docs" / "dockit.json").read_text(encoding="utf-8")
        )
        themes = (self.root / "docs" / "themes.md").read_text(encoding="utf-8")
        fixtures = (self.root / "docs" / "visual-fixtures.md").read_text(encoding="utf-8")

        self.assertEqual("docs/assets/visual-fixture-banner.svg", config["banner"]["path"])
        fixture_root = self.root / "examples" / "visual-fixtures"
        self.assertTrue((fixture_root / config["banner"]["path"]).is_file())
        self.assertIn("[visual fixture](visual-fixtures.md)", themes)
        self.assertIn("visual-fixture-banner.svg", fixtures)

    def test_theme_guide_points_to_maintained_exact_colour_and_style_examples(self) -> None:
        minimal = json.loads((self.root / "examples" / "minimal" / "docs" / "dockit.json").read_text(encoding="utf-8"))
        single_version = json.loads(
            (self.root / "examples" / "single-version" / "docs" / "dockit.json").read_text(encoding="utf-8")
        )
        themes = (self.root / "docs" / "themes.md").read_text(encoding="utf-8")

        self.assertEqual("#0f766e", minimal["theme"]["accent"])
        self.assertEqual("#0891b2", minimal["theme"]["accent_secondary"])
        self.assertEqual("paper", single_version["theme"]["style"])
        self.assertIn("[minimal example]", themes)
        self.assertIn("[single-version example]", themes)

    def test_configuration_documents_metadata_homepage_defaults_and_archives(self) -> None:
        configuration = (self.root / "docs" / "configuration.md").read_text(encoding="utf-8")
        checklist = (self.root / "docs" / "pre-publish-checklist.md").read_text(encoding="utf-8")
        fixture_guide = (self.root / "docs" / "visual-fixtures.md").read_text(encoding="utf-8")
        minimal = json.loads((self.root / "examples" / "minimal" / "docs" / "dockit.json").read_text(encoding="utf-8"))

        self.assertIn("becomes each generated page's description metadata", configuration)
        self.assertIn("does not render `repository_url` or `site_url`", configuration)
        self.assertIn("| `capabilities` | `true` |", configuration)
        self.assertIn("| `banner` | `true` |", configuration)
        self.assertIn("| `introduction` | `true` |", configuration)
        self.assertIn("| `release_context` | `false` |", configuration)
        self.assertIn("`--offline-archive`", checklist)
        self.assertIn("deterministic ZIP", checklist)
        self.assertEqual("compact", minimal["layout"]["content_width"])
        self.assertIn("maintained minimal example uses `compact`", configuration)
        self.assertIn("maintained minimal example uses `compact`", fixture_guide)

    def test_github_pages_guide_leads_with_the_one_command_setup_path(self) -> None:
        readme = (self.root / "README.md").read_text(encoding="utf-8")
        guide = (self.root / "docs" / "github-pages.md").read_text(encoding="utf-8")
        guide_words = " ".join(guide.split())

        self.assertIn("dockit-fp github-pages", readme)
        self.assertIn("## GitHub Pages in one command", guide)
        self.assertIn("Settings → Pages → Source → GitHub Actions", guide_words)
        self.assertIn("DocKit prepares GitHub; the maintainer controls Git.", guide)
        self.assertIn("dockit-fp github-pages --update", guide)
        self.assertIn("does not commit or push", guide)
        self.assertIn("## Advanced: manual and historical workflows", guide)

    def test_qualification_document_matches_the_ci_contract(self) -> None:
        qualification = (self.root / "docs" / "qualification.md").read_text(encoding="utf-8")
        readme = (self.root / "README.md").read_text(encoding="utf-8")
        ci = (self.root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

        self.assertIn("docs/qualification.md", readme)
        for version in ("3.10", "3.11", "3.12", "3.13", "3.14"):
            self.assertIn(version, qualification)
            self.assertIn(f"'{version}'", ci)
        for operating_system in ("Linux", "Windows", "macOS"):
            self.assertIn(operating_system, qualification)
        self.assertIn("wheel", qualification)
        self.assertIn("sdist", qualification)
        self.assertIn("## Manual browser/keyboard matrix", qualification)
        self.assertIn("# Qualification evidence for DocKit v1.0.0", qualification)
        self.assertIn("Browser automation status", qualification)

    def test_v1_five_promises_and_contract_are_explicit(self) -> None:
        readme = (self.root / "README.md").read_text(encoding="utf-8")
        roadmap = (self.root / "ROADMAP.md").read_text(encoding="utf-8")
        architecture = (self.root / "docs" / "architecture.md").read_text(encoding="utf-8")
        machine = (self.root / "docs" / "machine-contracts.md").read_text(encoding="utf-8")
        qualification = (self.root / "docs" / "qualification.md").read_text(encoding="utf-8")
        contributing = (self.root / "CONTRIBUTING.md").read_text(encoding="utf-8")
        decision = (self.root / "docs" / "decisions" / "0010-v1-stable-contract.md").read_text(encoding="utf-8")

        for promise in (
            "Easy to use", "Easy to learn", "Easy to look good",
            "Easy to create from existing repositories", "Easy to maintain",
        ):
            with self.subTest(promise=promise):
                self.assertIn(promise, readme + roadmap + qualification)
        self.assertIn("## v1.0 — Stable Contract", roadmap)
        self.assertIn("Release branches", contributing)
        self.assertIn("Compatibility policy", architecture)
        self.assertIn("Schema-version-1 configuration", machine)
        self.assertIn("1.x compatibility policy", machine)
        self.assertIn("0010", decision)

    def test_stable_contract_guides_and_examples_are_maintained(self) -> None:
        layout = json.loads((self.root / "docs" / "layout.json").read_text(encoding="utf-8"))
        pages = [page["path"] for section in layout["navigation"] for page in section["pages"]]
        machine = (self.root / "docs" / "machine-contracts.md").read_text(encoding="utf-8")
        custom_css = (self.root / "docs" / "custom-css.md").read_text(encoding="utf-8")
        themes = (self.root / "docs" / "themes.md").read_text(encoding="utf-8")
        configuration = (self.root / "docs" / "configuration.md").read_text(encoding="utf-8")
        fixture_config = json.loads(
            (self.root / "examples" / "visual-fixtures" / "docs" / "dockit.json").read_text(encoding="utf-8")
        )

        self.assertIn("custom-css.md", pages)
        self.assertIn("machine-contracts.md", pages)
        self.assertEqual("docs/assets/custom.css", fixture_config["theme"]["custom_css"])
        self.assertTrue((self.root / "examples" / "visual-fixtures" / "docs" / "assets" / "custom.css").is_file())
        self.assertIn("--dk-accent", custom_css)
        self.assertIn("schema_version", machine)
        self.assertIn("search-index.json", machine)
        self.assertIn("--dk-focus-ring", themes)
        self.assertIn("theme.custom_css", custom_css)
        self.assertIn("theme.custom_css", configuration)
        self.assertIn("Did you mean", configuration)
        self.assertIn("stable customisation contract", machine)

    def test_migration_guide_covers_every_release_through_v018_and_the_10_checklist(self) -> None:
        migration = (self.root / "docs" / "migration.md").read_text(encoding="utf-8")

        for release in ("v0.1.0", "v0.2.0", "v0.3.0", "v0.4.0", "v0.5.0", "v0.6.0", "v0.7.0",
                        "v0.8.0", "v0.9.0", "v0.10.0", "v0.11.0", "v0.12.0", "v0.13.0", "v0.14.0",
                        "v0.15.0", "v0.16.0", "v0.17.0", "v0.18.0"):
            self.assertIn(release, migration, release)
        self.assertIn("v0.17.0 to v0.18.0", migration)
        self.assertIn("--dk-bg", migration)
        self.assertIn("search-index.json", migration)
        self.assertIn("## 0.x to 1.0 upgrade checklist", migration)
        self.assertIn("v1.0.0", migration)

    def test_init_guidance_documents_the_declarative_mental_model(self) -> None:
        readme = (self.root / "README.md").read_text(encoding="utf-8")

        self.assertIn("The mental model from here on", readme)
        self.assertIn("layout.json", readme)
        self.assertIn("dockit.json", readme)
        self.assertIn("DocKit commands for editing pages, sections or themes", readme)
