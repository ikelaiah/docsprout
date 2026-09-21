"""Compatibility corpus: valid released schema-1 configuration keeps working.

Every scenario mirrors the actual published configuration of a released tag
(v0.1.0 through v0.17.0). The claim is not byte-identical output; it is that
valid supported historical schema-1 configuration is understood by current
DocSprout, or has an explicitly documented migration requirement. The corpus
deliberately keeps the pre-rebrand ``dockit.json`` filename because loading it
is part of the 1.x compatibility contract.
"""

import json
from pathlib import Path
import tempfile
import unittest

from docsprout.build import build_site
from docsprout.config import load_config
from docsprout.versions import load_manifest


CORPUS = {
    "v0.1.0-project-and-navigation": {
        "dockit.json": {
            "schema_version": 1,
            "project": {
                "name": "DocKit-FP",
                "description": "Versioned documentation sites for Free Pascal projects.",
                "repository_url": "https://github.com/ikelaiah/dockit-fp",
                "site_url": "https://ikelaiah.github.io/dockit-fp",
            },
            "theme": {"accent": "#4f46e5", "accent_secondary": "#0891b2"},
        },
        "layout.json": {
            "schema_version": 1,
            "navigation": [{"title": "Get started", "pages": [
                {"title": "Overview", "path": "index.md"},
            ]}],
        },
    },
    "v0.6.0-homepage": {
        "dockit.json": {
            "schema_version": 1,
            "project": {"name": "DocKit-FP"},
            "theme": {"accent": "#4f46e5", "accent_secondary": "#0891b2"},
            "homepage": {
                "capabilities": [
                    {"title": "Existing-project friendly", "description": "Start with the README and docs you already have."},
                ],
                "sections": {"release_context": True},
            },
        },
        "layout.json": {
            "schema_version": 1,
            "navigation": [{"title": "Start here", "pages": [
                {"title": "Overview", "path": "index.md"},
            ]}],
        },
    },
    "v0.8.0-content-width": {
        "dockit.json": {
            "schema_version": 1,
            "project": {"name": "DocKit-FP", "description": "Friendly, versioned code documentation."},
            "theme": {"accent": "#4f46e5", "accent_secondary": "#0891b2"},
            "layout": {"content_width": "wide"},
        },
        "layout.json": {
            "schema_version": 1,
            "navigation": [{"title": "Docs", "pages": [
                {"title": "Overview", "path": "index.md"},
            ]}],
        },
    },
    "v0.11.0-long-navigation": {
        "dockit.json": {
            "schema_version": 1,
            "project": {"name": "DocKit-FP", "description": "Friendly, versioned code documentation with a Free Pascal focus."},
            "theme": {"accent": "#4f46e5", "accent_secondary": "#0891b2"},
        },
        "layout.json": {
            "schema_version": 1,
            "navigation": [
                {"title": "Start here", "pages": [{"title": "Overview", "path": "index.md"}]},
                {"title": "Publish safely", "pages": [{"title": "GitHub Pages", "path": "github-pages.md"}]},
            ],
        },
    },
    "v0.12.1-identity-logo": {
        "dockit.json": {
            "schema_version": 1,
            "project": {"name": "DocKit"},
            "theme": {"preset": "purple"},
            "identity": {"logo": "docs/assets/dockit-mark.svg"},
        },
        "layout.json": {
            "schema_version": 1,
            "home": {"path": "index.md"},
            "navigation": [{"title": "Start here", "pages": [
                {"title": "Overview", "path": "index.md"},
            ]}],
        },
    },
    "v0.14.0-home-and-explicit-home": {
        "dockit.json": {
            "schema_version": 1,
            "project": {"name": "DocKit"},
            "theme": {"accent": "#4f46e5", "accent_secondary": "#0891b2"},
            "homepage": {
                "capabilities": [
                    {"title": "Versioned documentation", "description": "Keep released guides available side by side."},
                ],
                "sections": {"release_context": True},
            },
        },
        "layout.json": {
            "schema_version": 1,
            "home": {"path": "index.md"},
            "navigation": [{"title": "Start here", "pages": [
                {"title": "Overview", "path": "index.md"},
            ]}],
        },
    },
    "v0.17.0-full-identity-and-exclude": {
        "dockit.json": {
            "schema_version": 1,
            "project": {
                "name": "DocKit",
                "description": "Offline-friendly Markdown documentation sites for code projects, with a Pascal-friendly origin.",
                "repository_url": "https://github.com/ikelaiah/dockit-fp",
                "site_url": "https://ikelaiah.github.io/dockit-fp",
            },
            "theme": {"preset": "purple"},
            "identity": {
                "logo": "docs/assets/dockit-mark.svg",
                "footer": "Built with DocKit.",
                "links": [{"label": "Project", "url": "https://github.com/ikelaiah/dockit-fp"}],
            },
            "homepage": {
                "capabilities": [
                    {"title": "Existing-project friendly", "description": "Start with the README and docs you already have."},
                    {"title": "Polished with little setup", "description": "Build a searchable documentation site from Markdown."},
                ],
                "sections": {"release_context": True},
            },
        },
        "layout.json": {
            "schema_version": 1,
            "home": {"path": "index.md"},
            "unlisted": "exclude",
            "navigation": [{"title": "Start here", "pages": [
                {"title": "Overview", "path": "index.md"},
            ]}],
        },
    },
}


class HistoricalConfigurationCorpusTests(unittest.TestCase):
    def _write(self, root: Path, scenario: str, *, with_manifest: bool = False) -> None:
        docs = root / "docs"
        docs.mkdir(parents=True)
        (docs / "index.md").write_text("# Overview\n\nContent.", encoding="utf-8")
        (docs / "assets").mkdir()
        (docs / "assets" / "dockit-mark.svg").write_text("<svg/>", encoding="utf-8")
        for name, value in CORPUS[scenario].items():
            (docs / name).write_text(json.dumps(value), encoding="utf-8")
        for section in CORPUS[scenario]["layout.json"]["navigation"]:
            for page in section["pages"]:
                if page["path"] != "index.md":
                    target = docs / page["path"]
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(f"# {page['title']}\n\nContent.", encoding="utf-8")
        if with_manifest:
            (docs / "versions.json").write_text(json.dumps({
                "schema_version": 1, "current": "0.1.0", "versions": [
                    {"release": "0.1.0", "source_ref": "v0.1.0"},
                ],
            }), encoding="utf-8")

    def test_every_historical_scenario_loads_and_builds(self) -> None:
        for scenario in CORPUS:
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self._write(root, scenario)
                config = load_config(root)
                self.assertEqual("index.md", config.home_document)
                self.assertGreaterEqual(len(config.pages), 1)
                result = build_site(root=root, output=root / "site", release="0.18.0")
                self.assertGreaterEqual(result.page_count, 1)
                self.assertIn("Overview", (root / "site" / "index.html").read_text(encoding="utf-8"))

    def test_historical_versions_manifest_loads(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write(root, "v0.1.0-project-and-navigation", with_manifest=True)

            manifest = load_manifest(root)

            self.assertEqual("0.1.0", manifest.current)
            self.assertEqual((("0.1.0", "v0.1.0"),), tuple((entry.release, entry.source_ref) for entry in manifest.versions))