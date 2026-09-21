"""Rebrand compatibility: canonical DocSprout paths plus deprecated aliases."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from docsprout import __version__

from tests.helper import cli_environment
from tests.helper import SOURCE


def _run(module: str, root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", module, *arguments, "--root", str(root)],
        cwd=str(root), capture_output=True, text=True, encoding="utf-8",
        env=cli_environment(), timeout=90,
    )


def _write_project(root: Path, *, filename: str = "docsprout.json") -> None:
    docs = root / "docs"
    docs.mkdir()
    (docs / "index.md").write_text("# Home\n", encoding="utf-8")
    (docs / filename).write_text(
        json.dumps({"schema_version": 1, "project": {"name": "Compatibility"}}), encoding="utf-8",
    )
    (docs / "layout.json").write_text(json.dumps({
        "schema_version": 1,
        "navigation": [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}]}],
    }), encoding="utf-8")


class RebrandCompatibilityTests(unittest.TestCase):
    def test_canonical_module_reports_the_canonical_version(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run(
                [sys.executable, "-m", "docsprout", "--version"],
                capture_output=True, text=True, encoding="utf-8", env=cli_environment(), timeout=60,
            )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(f"docsprout {__version__}", result.stdout.strip())

    def test_deprecated_module_alias_still_answers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run(
                [sys.executable, "-m", "dockit_fp", "--version"],
                capture_output=True, text=True, encoding="utf-8", env=cli_environment(), timeout=60,
            )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(f"dockit-fp {__version__}", result.stdout.strip())
        self.assertIn("deprecated", result.stderr)

    def test_deprecated_package_exposes_public_version_metadata(self) -> None:
        result = subprocess.run(
            [sys.executable, "-c", "import dockit_fp; print(dockit_fp.__version__)"],
            capture_output=True, text=True, encoding="utf-8", env=cli_environment(), timeout=60,
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(__version__, result.stdout.strip())

    def test_legacy_dockit_json_project_checks_and_builds(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _write_project(root, filename="dockit.json")

            check = _run("docsprout", root, "check")
            build = _run("docsprout", root, "build", "--output", str(root / "site"))

            self.assertEqual(0, check.returncode, check.stdout + check.stderr)
            self.assertIn("Documentation check passed", check.stdout)
            self.assertEqual(0, build.returncode, build.stdout + build.stderr)
            self.assertTrue((root / "site" / ".docsprout-site").is_file())
            self.assertFalse((root / "site" / ".dockit-fp-site").exists())

    def test_legacy_marker_is_recognised_and_replaced_on_rebuild(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _write_project(root)
            site = root / "site"
            site.mkdir()
            (site / ".dockit-fp-site").write_text("DocKit-FP generated output.\n", encoding="utf-8")
            (site / "stale.html").write_text("stale", encoding="utf-8")

            build = _run("docsprout", root, "build", "--output", str(site))

            self.assertEqual(0, build.returncode, build.stdout + build.stderr)
            self.assertFalse((site / "stale.html").exists())
            self.assertTrue((site / ".docsprout-site").is_file())
            self.assertFalse((site / ".dockit-fp-site").exists())

    def test_both_configuration_names_fail_with_an_actionable_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _write_project(root)
            (root / "docs" / "dockit.json").write_text(
                json.dumps({"schema_version": 1, "project": {"name": "Legacy"}}), encoding="utf-8",
            )

            check = _run("docsprout", root, "check")

            self.assertEqual(1, check.returncode)
            self.assertIn("both docsprout.json and dockit.json exist", check.stdout)
            self.assertIn("docsprout.json", check.stdout)
            self.assertIn("dockit.json", check.stdout)

    def test_source_checkout_keeps_the_shim_importable(self) -> None:
        self.assertTrue((SOURCE / "dockit_fp" / "__init__.py").is_file())
        self.assertTrue((SOURCE / "dockit_fp" / "__main__.py").is_file())
        self.assertTrue((SOURCE / "docsprout" / "__init__.py").is_file())
