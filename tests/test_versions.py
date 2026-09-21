import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from docsprout.errors import DocSproutError
from docsprout.versions import build_all, check_release, load_manifest


class VersionedBuildTests(unittest.TestCase):
    def _git(self, root: Path, *arguments: str) -> None:
        subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True, text=True)

    def _repository(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self._git(root, "init")
        self._git(root, "config", "user.email", "tests@example.test")
        self._git(root, "config", "user.name", "Tests")
        docs = root / "docs"
        docs.mkdir()
        (docs / "README.md").write_text("# Version one\n\nOld content.", encoding="utf-8")
        self._git(root, "add", ".")
        self._git(root, "commit", "-m", "v1")
        self._git(root, "tag", "v1.0.0")
        (docs / "new.md").write_text("# Version two\n\nNew content.", encoding="utf-8")
        (docs / "versions.json").write_text(json.dumps({
            "schema_version": 1, "current": "2.0.0", "versions": [
                {"release": "2.0.0", "source_ref": "v2.0.0"},
                {"release": "1.0.0", "source_ref": "v1.0.0"},
            ],
        }), encoding="utf-8")
        self._git(root, "add", ".")
        self._git(root, "commit", "-m", "v2")
        self._git(root, "tag", "v2.0.0")
        return root

    def _modern_history_repository(self) -> Path:
        """Create an old modern release authored before strict navigation checks."""
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self._git(root, "init")
        self._git(root, "config", "user.email", "tests@example.test")
        self._git(root, "config", "user.name", "Tests")
        docs = root / "docs"
        docs.mkdir()
        (docs / "index.md").write_text("# Version one\n\nOld content.", encoding="utf-8")
        (docs / "archive.md").write_text("# Archived note\n\nOld navigation did not list this.", encoding="utf-8")
        (docs / "docsprout.json").write_text(json.dumps({
            "schema_version": 1,
            "project": {"name": "Historical docs"},
        }), encoding="utf-8")
        (docs / "layout.json").write_text(json.dumps({
            "schema_version": 1,
            "navigation": [{"title": "Docs", "pages": [
                {"title": "Overview", "path": "index.md"},
            ]}],
        }), encoding="utf-8")
        self._git(root, "add", ".")
        self._git(root, "commit", "-m", "v1")
        self._git(root, "tag", "v1.0.0")
        (docs / "private.md").write_text("# Private current note", encoding="utf-8")
        (docs / "layout.json").write_text(json.dumps({
            "schema_version": 1,
            "unlisted": "exclude",
            "navigation": [{"title": "Docs", "pages": [
                {"title": "Overview", "path": "index.md"},
                {"title": "Archive", "path": "archive.md"},
            ]}],
        }), encoding="utf-8")
        (docs / "versions.json").write_text(json.dumps({
            "schema_version": 1, "current": "2.0.0", "versions": [
                {"release": "2.0.0", "source_ref": "v2.0.0"},
                {"release": "1.0.0", "source_ref": "v1.0.0"},
            ],
        }), encoding="utf-8")
        self._git(root, "add", ".")
        self._git(root, "commit", "-m", "v2")
        self._git(root, "tag", "v2.0.0")
        return root

    def test_build_all_uses_each_tag_not_the_current_worktree(self) -> None:
        root = self._repository()
        result = build_all(root=root, output=root / "site")

        self.assertEqual(2, result.release_count)
        old_site = root / "site" / "1.0.0"
        self.assertTrue((old_site / "index.html").exists())
        self.assertFalse((old_site / "new.html").exists())
        self.assertNotIn("New content", (old_site / "index.html").read_text(encoding="utf-8"))
        self.assertIn("Version one", (old_site / "index.html").read_text(encoding="utf-8"))
        self.assertIn('value="../2.0.0/index.html"', (old_site / "index.html").read_text(encoding="utf-8"))

    def test_build_all_allows_unlisted_documents_in_historical_modern_releases(self) -> None:
        root = self._modern_history_repository()

        result = build_all(root=root, output=root / "site")

        self.assertEqual(2, result.release_count)
        self.assertTrue((root / "site" / "1.0.0" / "index.html").exists())

    def test_build_all_does_not_publish_currently_excluded_documents(self) -> None:
        root = self._modern_history_repository()

        build_all(root=root, output=root / "site")

        self.assertTrue((root / "site" / "2.0.0" / "archive.html").is_file())
        self.assertFalse((root / "site" / "2.0.0" / "private.html").exists())

    def test_build_all_reads_root_readmes_from_each_historical_source(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self._git(root, "init")
        self._git(root, "config", "user.email", "tests@example.test")
        self._git(root, "config", "user.name", "Tests")
        docs = root / "docs"
        docs.mkdir()
        (root / "README.md").write_text("# Version one", encoding="utf-8")
        (docs / "docsprout.json").write_text(json.dumps({"schema_version": 1, "project": {"name": "Demo"}}), encoding="utf-8")
        (docs / "layout.json").write_text(json.dumps({"schema_version": 1, "navigation": [{"title": "Overview", "pages": [{"title": "Overview", "path": "README.md", "source": "root"}]}]}), encoding="utf-8")
        self._git(root, "add", ".")
        self._git(root, "commit", "-m", "v1")
        self._git(root, "tag", "v1.0.0")
        (root / "README.md").write_text("# Version two", encoding="utf-8")
        (docs / "versions.json").write_text(json.dumps({"schema_version": 1, "current": "2.0.0", "versions": [
            {"release": "2.0.0", "source_ref": "v2.0.0"}, {"release": "1.0.0", "source_ref": "v1.0.0"},
        ]}), encoding="utf-8")
        self._git(root, "add", ".")
        self._git(root, "commit", "-m", "v2")
        self._git(root, "tag", "v2.0.0")

        build_all(root=root, output=root / "site")

        self.assertIn("Version one", (root / "site" / "1.0.0" / "index.html").read_text(encoding="utf-8"))
        self.assertIn("Version two", (root / "site" / "2.0.0" / "index.html").read_text(encoding="utf-8"))

    def test_check_release_rejects_moving_refs(self) -> None:
        root = self._repository()
        manifest = root / "docs" / "versions.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["versions"][0]["source_ref"] = "main"
        manifest.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaisesRegex(DocSproutError, "moving source_ref"):
            check_release(root)

    def test_manifest_rejects_unsafe_release_paths_and_git_option_refs(self) -> None:
        root = self._repository()
        manifest = root / "docs" / "versions.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["versions"][0]["release"] = "../outside"
        manifest.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaisesRegex(DocSproutError, r"versions\[0\]\.release.*safe name"):
            load_manifest(root)

        data["versions"][0]["release"] = "2.0.0"
        data["versions"][0]["source_ref"] = "--help"
        manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(DocSproutError, r"versions\[0\]\.source_ref.*tag or full commit SHA"):
            load_manifest(root)

    def test_manifest_rejects_unknown_fields_with_a_typo_suggestion(self) -> None:
        root = self._repository()
        manifest = root / "docs" / "versions.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["versionz"] = data.pop("versions")
        manifest.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaisesRegex(DocSproutError, r"Unknown field 'versions\.versionz'\. Did you mean 'versions\.versions'\?"):
            load_manifest(root)

        data["versionz"] = [{"release": "2.0.0", "source_ref": "v2.0.0", "changelog": "notes.md"}]
        data["versions"] = data.pop("versionz")
        manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(DocSproutError, r"Unknown field 'versions\[0\]\.changelog'"):
            load_manifest(root)

    def test_check_release_requires_current_source_to_match_head(self) -> None:
        root = self._repository()
        (root / "README.md").write_text("post-release change", encoding="utf-8")
        self._git(root, "add", "README.md")
        self._git(root, "commit", "-m", "move past release")

        with self.assertRaisesRegex(DocSproutError, r"current release '2\.0\.0'.*does not match HEAD"):
            check_release(root)

    def test_check_release_explains_how_to_create_a_missing_tag(self) -> None:
        root = self._repository()
        manifest = root / "docs" / "versions.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["versions"][0]["source_ref"] = "v2.0.1"
        manifest.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaisesRegex(DocSproutError, r"does not exist.*Create the tag"):
            check_release(root)

    def test_check_release_rejects_uncommitted_documentation(self) -> None:
        root = self._repository()
        (root / "docs" / "new.md").write_text("# Changed after tagging", encoding="utf-8")

        with self.assertRaisesRegex(DocSproutError, r"Documentation differs from HEAD.*Commit docs changes"):
            check_release(root)

    def test_build_all_avoids_the_pre_312_incompatible_extractall_filter_keyword(self) -> None:
        import tarfile
        from types import SimpleNamespace
        from unittest.mock import patch

        import docsprout.versions as versions_module

        root = self._repository()
        received: dict = {}
        original_extractall = tarfile.TarFile.extractall

        def recording_extractall(self_, path=".", members=None, *, numeric_owner=False, **kwargs):
            received.update(kwargs)
            return original_extractall(self_, path, members, numeric_owner=numeric_owner)

        with patch("tarfile.TarFile.extractall", new=recording_extractall), patch.object(
            versions_module, "sys", SimpleNamespace(version_info=(3, 11, 0, "final", 0))
        ):
            result = build_all(root=root, output=root / "site")

        self.assertEqual(2, result.release_count)
        self.assertEqual({}, received)
        self.assertIn("Version one", (root / "site" / "1.0.0" / "index.html").read_text(encoding="utf-8"))

    def test_historical_example_build_is_byte_for_byte_deterministic(self) -> None:
        example = Path(__file__).resolve().parents[1] / "examples" / "historical"
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self._git(root, "init")
        self._git(root, "config", "user.email", "tests@example.test")
        self._git(root, "config", "user.name", "Tests")
        shutil.copytree(example / "releases" / "v1.0.0" / "docs", root / "docs")
        self._git(root, "add", ".")
        self._git(root, "commit", "-m", "release 1.0.0")
        self._git(root, "tag", "v1.0.0")
        shutil.rmtree(root / "docs")
        shutil.copytree(example / "docs", root / "docs")
        self._git(root, "add", ".")
        self._git(root, "commit", "-m", "release 1.1.0")
        self._git(root, "tag", "v1.1.0")

        first, second = root / "site-first", root / "site-second"
        build_all(root=root, output=first)
        build_all(root=root, output=second)
        first_files = {path.relative_to(first): path.read_bytes() for path in first.rglob("*") if path.is_file()}
        second_files = {path.relative_to(second): path.read_bytes() for path in second.rglob("*") if path.is_file()}

        self.assertEqual(first_files, second_files)
        self.assertTrue((first / "1.1.0" / "upgrade.html").exists())
        self.assertFalse((first / "1.0.0" / "upgrade.html").exists())
