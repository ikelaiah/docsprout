import io
from contextlib import redirect_stdout
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from docsprout.cli import _PreviewBuilder, main


class CliTests(unittest.TestCase):
    def _git(self, root: Path, *arguments: str) -> None:
        subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True, text=True)

    def test_init_creates_a_non_destructive_minimal_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(0, main(["init", "--root", str(root)]))
            self.assertTrue((root / "docs" / "docsprout.json").exists())
            layout = json.loads((root / "docs" / "layout.json").read_text(encoding="utf-8"))
            self.assertEqual({"path": "index.md"}, layout["home"])
            self.assertEqual("exclude", layout["unlisted"])
            self.assertIn("DocSprout is ready.", output.getvalue())
            self.assertIn("docs/layout.json", output.getvalue())
            self.assertIn("docs/docsprout.json", output.getvalue())
            self.assertIn("Preview:  docsprout serve", output.getvalue())
            self.assertIn("Navigation sections: Getting started (1 page).", output.getvalue())
            self.assertEqual(0, main(["init", "--root", str(root)]))

    def test_init_adopts_a_readme_and_nested_docs_without_publishing_ancillary_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            (docs / "getting-started").mkdir(parents=True)
            readme = root / "README.md"
            readme.write_text("# Existing project", encoding="utf-8")
            (docs / "getting-started" / "quick-start.md").write_text("# Quick start", encoding="utf-8")
            (docs / "reference.md").write_text("# API", encoding="utf-8")
            changelog = root / "CHANGELOG.md"
            changelog.write_text("# Changes", encoding="utf-8")
            contributing = root / "CONTRIBUTING.md"
            contributing.write_text("# Contributing", encoding="utf-8")
            before = {path: path.read_text(encoding="utf-8") for path in (readme, changelog, contributing, docs / "getting-started" / "quick-start.md", docs / "reference.md")}
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(0, main(["init", "--root", str(root)]))

            layout = json.loads((docs / "layout.json").read_text(encoding="utf-8"))
            self.assertEqual("exclude", layout["unlisted"])
            pages = [page for section in layout["navigation"] for page in section["pages"]]
            self.assertEqual(
                [
                    {"title": "Overview", "path": "README.md", "source": "root"},
                    {"title": "Quick Start", "path": "getting-started/quick-start.md"},
                    {"title": "Reference", "path": "reference.md"},
                ],
                pages,
            )
            self.assertIn("Available for explicit inclusion: CHANGELOG.md, CONTRIBUTING.md", output.getvalue())
            self.assertEqual(before, {path: path.read_text(encoding="utf-8") for path in before})

    def test_init_uses_github_remote_metadata_and_leaves_an_existing_layout_authoritative(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._git(root, "init")
            self._git(root, "remote", "add", "origin", "git@github.com:example/existing-project.git")
            docs = root / "docs"
            docs.mkdir()
            (root / "README.md").write_text("# Existing", encoding="utf-8")
            (docs / "index.md").write_text("# Documentation", encoding="utf-8")
            (docs / "layout.json").write_text(
                '{"schema_version": 1, "navigation": [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}]}]}\n',
                encoding="utf-8",
            )
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(0, main(["init", "--root", str(root)]))
            config = json.loads((docs / "docsprout.json").read_text(encoding="utf-8"))
            self.assertEqual("existing-project", config["project"]["name"])
            self.assertEqual("https://github.com/example/existing-project", config["project"]["repository_url"])

            layout_before = (docs / "layout.json").read_text(encoding="utf-8")
            (docs / "new.md").write_text("# New", encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(0, main(["init", "--root", str(root)]))
            self.assertEqual(layout_before, (docs / "layout.json").read_text(encoding="utf-8"))

    def test_init_keeps_an_existing_docs_index_and_excludes_arbitrary_root_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Existing docs home", encoding="utf-8")
            notes = root / "NOTES.md"
            notes.write_text("# Private notes", encoding="utf-8")

            self.assertEqual(0, main(["init", "--root", str(root)]))

            layout = json.loads((docs / "layout.json").read_text(encoding="utf-8"))
            paths = [page["path"] for section in layout["navigation"] for page in section["pages"]]
            self.assertEqual(["index.md"], paths)
            self.assertEqual("# Existing docs home", (docs / "index.md").read_text(encoding="utf-8"))
            self.assertNotIn("NOTES.md", paths)

    def test_serve_validates_then_serves_on_the_requested_host_and_port(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(0, main(["init", "--root", str(root)]))
            events: list[tuple[str, object]] = []

            class Server:
                def serve_forever(self) -> None:
                    events.append(("serve", None))

                def server_close(self) -> None:
                    events.append(("close", None))

            def make_server(address, handler):
                events.append(("address", address))
                return Server()

            output = io.StringIO()
            with patch("docsprout.cli.ThreadingHTTPServer", side_effect=make_server):
                with redirect_stdout(output):
                    self.assertEqual(0, main(["serve", "--root", str(root), "--host", "127.0.0.1", "--port", "8000"]))

            self.assertEqual(("address", ("127.0.0.1", 8000)), events[0])
            self.assertEqual(["serve", "close"], [event[0] for event in events[1:]])
            self.assertIn("Serving documentation at http://127.0.0.1:8000/", output.getvalue())

    def test_preview_rebuilds_when_documentation_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(0, main(["init", "--root", str(root)]))
            preview = _PreviewBuilder(root=root, output=root / "build" / "docs-site", release="preview")
            preview.build_initial()

            (root / "docs" / "index.md").write_text("# Updated preview\n\nThe rebuilt page is current.", encoding="utf-8")

            self.assertTrue(preview.rebuild_if_changed())
            self.assertIn("Updated preview", (root / "build" / "docs-site" / "index.html").read_text(encoding="utf-8"))
            self.assertFalse(preview.rebuild_if_changed())

    def test_preview_rebuilds_when_renderer_source_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(0, main(["init", "--root", str(root)]))
            renderer = root / "renderer.py"
            renderer.write_text("first renderer", encoding="utf-8")
            preview = _PreviewBuilder(
                root=root,
                output=root / "build" / "docs-site",
                release="preview",
                renderer_sources=(renderer,),
            )
            preview.build_initial()

            renderer.write_text("updated renderer", encoding="utf-8")

            with patch("docsprout.cli.importlib.reload") as reload:
                self.assertTrue(preview.rebuild_if_changed())
            self.assertTrue(reload.called)

    def test_preview_rebuilds_when_layout_or_docsprout_configuration_changes(self) -> None:
        for configuration in ("layout.json", "docsprout.json"):
            with self.subTest(configuration=configuration), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.assertEqual(0, main(["init", "--root", str(root)]))
                preview = _PreviewBuilder(root=root, output=root / "build" / "docs-site", release="preview")
                preview.build_initial()

                document = root / "docs" / configuration
                data = json.loads(document.read_text(encoding="utf-8"))
                if configuration == "layout.json":
                    data["navigation"][0]["pages"].append(
                        {"title": "Reference", "path": "reference.md"},
                    )
                    (root / "docs" / "reference.md").write_text("# Reference\n\nContent.", encoding="utf-8")
                else:
                    data["theme"] = {"preset": "purple"}
                document.write_text(json.dumps(data), encoding="utf-8")

                self.assertTrue(preview.rebuild_if_changed(), configuration)
                built = (root / "build" / "docs-site" / "index.html").read_text(encoding="utf-8")
                if configuration == "layout.json":
                    self.assertIn("Reference", built)
                else:
                    self.assertIn("--dk-accent:#7c3aed", built)
                self.assertFalse(preview.rebuild_if_changed())

    def test_the_public_cli_surface_lists_only_operational_commands(self) -> None:
        commands = ("init", "serve", "check", "audit", "build", "build-all", "check-release", "github-pages", "doctor")
        with redirect_stdout(io.StringIO()) as help_output:
            with self.assertRaises(SystemExit) as exit_code:
                main(["--help"])
        self.assertEqual(0, exit_code.exception.code)
        help_text = help_output.getvalue()
        for command in commands:
            self.assertIn(command, help_text)
        for command, options in (
            ("build", ("--output", "--release", "--offline-archive")),
            ("build-all", ("--output",)),
            ("serve", ("--host", "--port")),
            ("github-pages", ("--update",)),
            ("audit", ("--strict", "--format")),
        ):
            with self.subTest(command=command), redirect_stdout(io.StringIO()) as command_help:
                with self.assertRaises(SystemExit):
                    main([command, "--help"])
            for option in options:
                self.assertIn(option, command_help.getvalue())
            self.assertIn("--root", command_help.getvalue())

    def test_serve_does_not_start_when_validation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "docsprout.json").write_text('{"schema_version": 1, "project": {"name": "Broken"}}', encoding="utf-8")
            with patch("docsprout.cli.ThreadingHTTPServer") as server:
                self.assertEqual(1, main(["serve", "--root", str(root)]))
            server.assert_not_called()

    def test_check_reports_excluded_markdown_concisely(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Home", encoding="utf-8")
            (docs / "private.md").write_text("# Private", encoding="utf-8")
            (docs / "docsprout.json").write_text('{"schema_version": 1, "project": {"name": "Demo"}}', encoding="utf-8")
            (docs / "layout.json").write_text('{"schema_version": 1, "unlisted": "exclude", "navigation": [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}]}]}', encoding="utf-8")
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(0, main(["check", "--root", str(root)]))

            self.assertIn("1 unlisted document(s) excluded", output.getvalue())

    def test_doctor_explains_the_next_preview_step(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(0, main(["init", "--root", str(root)]))
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(0, main(["doctor", "--root", str(root)]))

            self.assertIn("Status: preview-ready", output.getvalue())
            self.assertIn("Next: run docsprout serve.", output.getvalue())

    def test_doctor_explains_the_next_release_step(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(0, main(["init", "--root", str(root)]))
            (root / "docs" / "versions.json").write_text(
                '{"schema_version": 1, "current": "0.2.0", "versions": [{"release": "0.2.0", "source_ref": "v0.2.0"}]}',
                encoding="utf-8",
            )
            self._git(root, "init")
            self._git(root, "config", "user.email", "tests@example.test")
            self._git(root, "config", "user.name", "Tests")
            self._git(root, "add", ".")
            self._git(root, "commit", "-m", "release")
            self._git(root, "tag", "v0.2.0")
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(0, main(["doctor", "--root", str(root)]))

            self.assertIn("Status: versioned release configured", output.getvalue())
            self.assertIn("Release refs: verified; current v0.2.0 matches HEAD", output.getvalue())
            self.assertIn("Next: follow the pre-publish checklist before publishing.", output.getvalue())

    def test_doctor_reports_a_missing_current_release_tag(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(0, main(["init", "--root", str(root)]))
            (root / "docs" / "versions.json").write_text(
                '{"schema_version": 1, "current": "0.9.0", "versions": [{"release": "0.9.0", "source_ref": "v0.9.0"}]}',
                encoding="utf-8",
            )
            self._git(root, "init")
            self._git(root, "config", "user.email", "tests@example.test")
            self._git(root, "config", "user.name", "Tests")
            self._git(root, "add", ".")
            self._git(root, "commit", "-m", "prepare release")
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(1, main(["doctor", "--root", str(root)]))

            self.assertIn("ERROR: Release refs:", output.getvalue())
            self.assertIn("Create the tag", output.getvalue())

    def test_check_and_build_report_success_for_initialized_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(0, main(["init", "--root", str(root)]))
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(0, main(["check", "--root", str(root)]))
            self.assertIn("Documentation check passed: 1 section(s), 1 page(s)", output.getvalue())
            self.assertEqual(0, main(["build", "--root", str(root), "--output", str(root / "site")]))
            self.assertTrue((root / "site" / "index.html").exists())

    def test_init_preserves_a_legacy_dockit_json_without_creating_a_second_config(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Home", encoding="utf-8")
            (docs / "dockit.json").write_text('{"schema_version": 1, "project": {"name": "Legacy"}}', encoding="utf-8")
            (docs / "layout.json").write_text(
                '{"schema_version": 1, "unlisted": "exclude", "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]}',
                encoding="utf-8",
            )
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(0, main(["init", "--root", str(root)]))

            self.assertFalse((docs / "docsprout.json").exists())
            self.assertTrue((docs / "dockit.json").exists())
            self.assertIn("Existing configuration was left authoritative", output.getvalue())
            self.assertIn("Change colours, logo and presentation:  docs/dockit.json", output.getvalue())
            self.assertIn("rename docs/dockit.json to docs/docsprout.json", output.getvalue())

    def test_check_fails_with_an_ambiguity_error_when_both_configurations_exist(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Home", encoding="utf-8")
            (docs / "docsprout.json").write_text('{"schema_version": 1, "project": {"name": "Current"}}', encoding="utf-8")
            (docs / "dockit.json").write_text('{"schema_version": 1, "project": {"name": "Legacy"}}', encoding="utf-8")
            (docs / "layout.json").write_text(
                '{"schema_version": 1, "unlisted": "exclude", "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]}',
                encoding="utf-8",
            )
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(1, main(["check", "--root", str(root)]))

            self.assertIn("both docsprout.json and dockit.json exist", output.getvalue())

    def test_doctor_names_the_legacy_configuration_file_and_rename_step(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / "index.md").write_text("# Home", encoding="utf-8")
            (docs / "dockit.json").write_text('{"schema_version": 1, "project": {"name": "Legacy"}}', encoding="utf-8")
            (docs / "layout.json").write_text(
                '{"schema_version": 1, "unlisted": "exclude", "navigation": [{"title": "Start", "pages": [{"title": "Home", "path": "index.md"}]}]}',
                encoding="utf-8",
            )
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(0, main(["doctor", "--root", str(root)]))

            self.assertIn("dockit.json uses the legacy configuration name", output.getvalue())
            self.assertIn("rename it to docs/docsprout.json", output.getvalue())
            self.assertIn("removed in v2.0.0", output.getvalue())

    def test_doctor_does_not_warn_for_the_canonical_configuration_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(0, main(["init", "--root", str(root)]))
            output = io.StringIO()

            with redirect_stdout(output):
                self.assertEqual(0, main(["doctor", "--root", str(root)]))

            self.assertNotIn("legacy configuration name", output.getvalue())
