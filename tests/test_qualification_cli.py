import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.request

from dockit_fp import __version__
from dockit_fp.github_pages import WORKFLOW_RELATIVE_PATH, render_workflow

from tests.helper import cli_environment, run_cli


def _free_port() -> int:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


class RealCliWorkflowQualificationTests(unittest.TestCase):
    def test_maintainer_journey_on_a_new_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)

            init = run_cli(root, "init")
            self.assertIn("Created: docs/dockit.json, docs/index.md, docs/layout.json.", init.stdout)
            self.assertIn("Next: run dockit-fp serve.", init.stdout)

            check = run_cli(root, "check")
            self.assertIn("Documentation check passed: 1 section(s), 1 page(s)", check.stdout)

            audit = run_cli(root, "audit", "--format", "json")
            report = json.loads(audit.stdout)
            self.assertEqual(0, report["errors"])
            self.assertEqual(0, report["warnings"])
            self.assertEqual(1, report["pages"])

            build = run_cli(root, "build", "--output", str(root / "site"))
            self.assertIn("Built 1 page(s)", build.stdout)
            site = root / "site"
            self.assertTrue((site / "index.html").is_file())
            self.assertIn("assets/katex/katex.min.js", (site / "index.html").read_text(encoding="utf-8"))
            self.assertTrue((site / "assets" / "katex" / "katex.min.js").is_file())
            self.assertTrue((site / "assets" / "katex" / "katex.min.css").is_file())
            self.assertTrue(any((site / "assets" / "katex" / "fonts").glob("*.woff2")))
            index = json.loads((site / "search-index.json").read_text(encoding="utf-8"))
            plain_name = re.sub(r"[*_`]+", "", root.name)
            self.assertEqual(
                [{"title": plain_name, "section": "Getting started", "url": "index.html", "text": f"{plain_name} Welcome to the documentation."}],
                index,
            )
            release = json.loads((site / "release.json").read_text(encoding="utf-8"))
            self.assertEqual("preview", release["release"])

            doctor = run_cli(root, "doctor")
            self.assertIn("Status: preview-ready", doctor.stdout)
            self.assertIn("Next: run dockit-fp serve.", doctor.stdout)

    def test_existing_repository_journey_publishes_only_the_listed_documents(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            for folder in ("guides", "images"):
                (docs / folder).mkdir(parents=True)
            readme = root / "README.md"
            readme.write_text("# Existing project\n\n[Guide](docs/guides/advanced.md)\n\n![Mark](docs/images/mark.svg)\n", encoding="utf-8")
            (docs / "index.md").write_text("# Documentation index", encoding="utf-8")
            (docs / "guides" / "advanced.md").write_text("# Advanced guide\n\n[Back](../../README.md)", encoding="utf-8")
            (docs / "release-notes.md").write_text("# Release notes\n\nInternal draft.", encoding="utf-8")
            (docs / "images" / "mark.svg").write_text("<svg/>", encoding="utf-8")
            (root / "CHANGELOG.md").write_text("# Changes", encoding="utf-8")
            (docs / "dockit.json").write_text(json.dumps({
                "schema_version": 1, "project": {"name": "Existing"}, "identity": {"footer": "Kept"},
            }), encoding="utf-8")
            (docs / "layout.json").write_text(json.dumps({
                "schema_version": 1, "unlisted": "exclude",
                "home": {"path": "README.md", "source": "root"},
                "navigation": [
                    {"title": "Overview", "pages": [{"title": "Overview", "path": "README.md", "source": "root"}]},
                    {"title": "Documentation", "pages": [
                        {"title": "Index", "path": "index.md"},
                        {"title": "Advanced", "path": "guides/advanced.md"},
                    ]},
                ],
            }), encoding="utf-8")
            before = {
                path: path.read_text(encoding="utf-8")
                for path in (readme, docs / "guides" / "advanced.md", docs / "layout.json", docs / "dockit.json")
            }

            adopted = run_cli(root, "init")
            self.assertIn("Existing DocKit configuration was left authoritative", adopted.stdout)
            self.assertEqual(before, {path: path.read_text(encoding="utf-8") for path in before})

            check = run_cli(root, "check")
            self.assertIn("Documentation check passed: 2 section(s), 3 page(s)", check.stdout)
            self.assertIn("1 unlisted document(s) excluded", check.stdout)

            audit = run_cli(root, "audit")
            self.assertIn("Errors: 0", audit.stdout)
            self.assertIn("Unpublished Markdown files: 1", audit.stdout)
            self.assertIn("Ready to publish.", audit.stdout)

            run_cli(root, "build", "--output", str(root / "site"))
            site = root / "site"
            self.assertIn("Existing project", (site / "index.html").read_text(encoding="utf-8"))
            self.assertIn("Advanced guide", (site / "guides" / "advanced.html").read_text(encoding="utf-8"))
            self.assertTrue((site / "docs-index.html").is_file())
            self.assertFalse((site / "release-notes.html").exists())
            self.assertTrue((site / "assets" / "content" / "images" / "mark.svg").is_file())
            search = json.loads((site / "search-index.json").read_text(encoding="utf-8"))
            self.assertEqual(
                ["index.html", "docs-index.html", "guides/advanced.html"],
                [entry["url"] for entry in search],
            )

    def test_serve_starts_serves_and_stops_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run_cli(root, "init")
            port = _free_port()
            server = subprocess.Popen(
                [sys.executable, "-u", "-m", "dockit_fp", "serve", "--root", str(root), "--port", str(port)],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                env=cli_environment(),
            )
            try:
                page = self._read_with_retries(port)
                self.assertIn("Welcome to the documentation.", page)
                self.assertIn("assets/katex/katex.min.css", page)
                css = self._read_with_retries(port, "/assets/site.css")
                self.assertIn("--dk-accent", css)
            finally:
                server.terminate()
                server.wait(timeout=15)
            log = ""
            if server.stdout:
                log = server.stdout.read()
                server.stdout.close()
            self.assertIn("Serving documentation at", log)

    def test_github_pages_qualifies_the_git_repository_release_walkthrough(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
            subprocess.run(
                ["git", "config", "user.email", "tests@example.test"], cwd=root, check=True, capture_output=True, text=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Tests"], cwd=root, check=True, capture_output=True, text=True,
            )
            subprocess.run(
                ["git", "remote", "add", "origin", "git@github.com:example/qualified-project.git"],
                cwd=root, check=True, capture_output=True, text=True,
            )
            (root / "README.md").write_text("# Qualified project\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=root, check=True, capture_output=True, text=True)
            subprocess.run(["git", "commit", "-m", "seed"], cwd=root, check=True, capture_output=True, text=True)
            header_before = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True,
            ).stdout

            prepared = run_cli(root, "github-pages")
            self.assertIn("DocKit is ready for GitHub Pages.", prepared.stdout)
            self.assertIn("Home: README.md", prepared.stdout)
            self.assertIn("git add .", prepared.stdout)
            workflow = self._expected_workflow()
            self.assertEqual(workflow, (root / WORKFLOW_RELATIVE_PATH).read_text(encoding="utf-8"))

            rerun = run_cli(root, "github-pages")
            self.assertIn("No changes required.", rerun.stdout)
            self.assertEqual(workflow, (root / WORKFLOW_RELATIVE_PATH).read_text(encoding="utf-8"))
            header_after = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True,
            ).stdout
            self.assertEqual(header_before, header_after)
            status = subprocess.run(
                ["git", "status", "--porcelain"], cwd=root, check=True, capture_output=True, text=True,
            ).stdout
            self.assertIn("?? docs/", status)
            self.assertIn("?? .github/", status)
            self.assertEqual(1, len(subprocess.run(
                ["git", "log", "--oneline"], cwd=root, check=True, capture_output=True, text=True,
            ).stdout.splitlines()))

            run_cli(root, "build", "--output", str(root / "site"))
            self.assertTrue((root / "site" / "index.html").is_file())

    def _expected_workflow(self) -> str:
        return render_workflow(f"v{__version__}")

    @staticmethod
    def _read_with_retries(port: int, path: str = "/", attempts: int = 40) -> str:
        url = f"http://127.0.0.1:{port}{path}"
        last_error: Exception | None = None
        for _ in range(attempts):
            try:
                with urllib.request.urlopen(url, timeout=3) as response:
                    return response.read().decode("utf-8")
            except Exception as error:  # noqa: BLE001 - retry while the server boots
                last_error = error
                time.sleep(0.25)
        raise AssertionError(f"server never answered {url}: {last_error}")