"""Qualification: DocKit behaves sensibly in the ecosystems it explicitly supports.

Non-Git projects, Git repositories, GitHub Pages preparation, idempotent reruns,
existing and generated configuration, and the no-commit/no-push rule. All tests
run fully offline: no GitHub API and no network access is required.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from dockit_fp import __version__
from dockit_fp.build import build_site
from dockit_fp.github_pages import WORKFLOW_RELATIVE_PATH, render_workflow

from tests.helper import run_cli


def _git(root: Path, *arguments: str) -> str:
    result = subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True, text=True)
    return result.stdout


class EcosystemQualificationTests(unittest.TestCase):
    def test_qualifies_an_ordinary_non_git_project_end_to_end(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "plain-project"
            root.mkdir()
            (root / "README.md").write_text("# Plain project\n", encoding="utf-8")

            initialised = run_cli(root, "init")
            self.assertIn("non-Git project", initialised.stdout)

            run_cli(root, "check")
            run_cli(root, "build", "--output", str(root / "site"))
            self.assertTrue((root / "site" / "index.html").is_file())

            refused = run_cli(root, "github-pages", check=False)
            self.assertEqual(1, refused.returncode)
            self.assertIn("not a Git repository", refused.stdout)

    def test_qualifies_a_git_repository_without_a_remote(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "local-repository"
            root.mkdir()
            _git(root, "init")
            _git(root, "config", "user.email", "tests@example.test")
            _git(root, "config", "user.name", "Tests")
            (root / "README.md").write_text("# Local repository\n", encoding="utf-8")
            _git(root, "add", ".")
            _git(root, "commit", "-m", "seed")

            prepared = run_cli(root, "github-pages")
            self.assertIn("not connected to GitHub yet", prepared.stdout)
            config = json.loads((root / "docs" / "dockit.json").read_text(encoding="utf-8"))
            self.assertNotIn("repository_url", config["project"])

    def test_qualifies_a_git_repository_with_a_github_remote(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "remote-repository"
            root.mkdir()
            _git(root, "init")
            _git(root, "config", "user.email", "tests@example.test")
            _git(root, "config", "user.name", "Tests")
            _git(root, "remote", "add", "origin", "git@github.com:acme/library.git")
            (root / "README.md").write_text("# Remote repository\n", encoding="utf-8")
            _git(root, "add", ".")
            _git(root, "commit", "-m", "seed")

            prepared = run_cli(root, "github-pages")
            self.assertIn("GitHub remote: https://github.com/acme/library", prepared.stdout)
            config = json.loads((root / "docs" / "dockit.json").read_text(encoding="utf-8"))
            self.assertEqual("https://github.com/acme/library", config["project"]["repository_url"])
            self.assertEqual("library", config["project"]["name"])

    def test_qualifies_idempotent_reruns_that_never_commit_or_push(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "idempotent-repository"
            root.mkdir()
            _git(root, "init")
            _git(root, "config", "user.email", "tests@example.test")
            _git(root, "config", "user.name", "Tests")
            (root / "README.md").write_text("# Idempotent\n", encoding="utf-8")
            _git(root, "add", ".")
            _git(root, "commit", "-m", "seed")
            head = _git(root, "rev-parse", "HEAD")

            first = run_cli(root, "github-pages")
            self.assertIn("DocKit is ready for GitHub Pages.", first.stdout)
            self.assertEqual(render_workflow(f"v{__version__}"), (root / WORKFLOW_RELATIVE_PATH).read_text(encoding="utf-8"))

            for _ in range(2):
                rerun = run_cli(root, "github-pages")
                self.assertIn("No changes required.", rerun.stdout)
                self.assertEqual(1, len(_git(root, "log", "--oneline").splitlines()))
                self.assertEqual(head, _git(root, "rev-parse", "HEAD"))
                self.assertEqual(
                    render_workflow(f"v{__version__}"),
                    (root / WORKFLOW_RELATIVE_PATH).read_text(encoding="utf-8"),
                )

            workflow = root / WORKFLOW_RELATIVE_PATH
            workflow.write_text(render_workflow("v0.12.1"), encoding="utf-8")
            run_cli(root, "github-pages")
            self.assertEqual(render_workflow("v0.12.1"), workflow.read_text(encoding="utf-8"))
            run_cli(root, "github-pages", "--update")
            self.assertEqual(render_workflow(f"v{__version__}"), workflow.read_text(encoding="utf-8"))
            self.assertEqual(head, _git(root, "rev-parse", "HEAD"))

    def test_qualifies_existing_supported_configuration_builds_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "existing-config"
            root.mkdir()
            docs = root / "docs"
            (docs / "guides").mkdir(parents=True)
            (docs / "index.md").write_text("# Existing home\n\n[Guide](guides/legacy.md)", encoding="utf-8")
            (docs / "guides" / "legacy.md").write_text("# Legacy guide\n\n[Back](../index.md)", encoding="utf-8")
            (docs / "dockit.json").write_text(json.dumps({
                "schema_version": 1,
                "project": {"name": "Existing", "description": "Kept"},
                "theme": {"preset": "teal", "style": "paper"},
            }), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({
                "schema_version": 1,
                "home": {"path": "index.md"},
                "navigation": [{"title": "Docs", "pages": [
                    {"title": "Home", "path": "index.md"},
                    {"title": "Legacy", "path": "guides/legacy.md"},
                ]}],
            }), encoding="utf-8")
            before = {path: path.read_text(encoding="utf-8") for path in (docs / "dockit.json", docs / "layout.json")}

            with tempfile.TemporaryDirectory() as output_temporary:
                result = build_site(root=root, output=Path(output_temporary) / "site", release="existing")

                self.assertEqual(2, result.page_count)
                self.assertEqual(before, {path: path.read_text(encoding="utf-8") for path in before})

    def test_qualifies_current_generated_configuration_on_top_of_github_pages(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "generated-config"
            root.mkdir()
            _git(root, "init")
            _git(root, "config", "user.email", "tests@example.test")
            _git(root, "config", "user.name", "Tests")
            _git(root, "remote", "add", "origin", "git@github.com:acme/generated.git")
            (root / "README.md").write_text("# Generated configuration\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
            _git(root, "add", ".")
            _git(root, "commit", "-m", "seed")

            run_cli(root, "github-pages")
            generated = json.loads((root / "docs" / "layout.json").read_text(encoding="utf-8"))
            self.assertEqual({"path": "README.md", "source": "root"}, generated["home"])
            self.assertEqual("exclude", generated["unlisted"])
            paths = [page["path"] for section in generated["navigation"] for page in section["pages"]]
            self.assertEqual(["README.md", "guide.md"], paths)

            check = run_cli(root, "check")
            self.assertIn("Documentation check passed", check.stdout)
            with tempfile.TemporaryDirectory() as output_temporary:
                build_site(root=root, output=Path(output_temporary) / "site", release="generated")
                self.assertTrue((Path(output_temporary) / "site" / "index.html").is_file())

    def test_doctor_detects_a_generated_managed_configuration_everywhere(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "doctor-project"
            root.mkdir()
            run_cli(root, "init")
            _git(root, "init")
            _git(root, "config", "user.email", "tests@example.test")
            _git(root, "config", "user.name", "Tests")
            _git(root, "add", ".")
            _git(root, "commit", "-m", "docs")
            run_cli(root, "github-pages")

            doctor = run_cli(root, "doctor")
            self.assertIn("Status: preview-ready", doctor.stdout)
            self.assertIn("GitHub Pages workflow: configured", doctor.stdout)
            self.assertIn(f"DocKit version: v{__version__}", doctor.stdout)