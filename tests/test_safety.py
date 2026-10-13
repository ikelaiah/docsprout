from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from docsprout.errors import DocSproutError
from docsprout.safety import OWNERSHIP_MARKER, prepare_output, staged_output


class OutputSafetyTests(unittest.TestCase):
    def test_staged_output_publishes_only_after_the_build_finishes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "site"
            prepare_output(output)
            (output / "old.html").write_text("old", encoding="utf-8")

            with staged_output(output) as staging:
                prepare_output(staging)
                (staging / "index.html").write_text("new", encoding="utf-8")
                self.assertEqual("old", (output / "old.html").read_text(encoding="utf-8"))
                self.assertFalse((output / "index.html").exists())

            self.assertFalse((output / "old.html").exists())
            self.assertEqual("new", (output / "index.html").read_text(encoding="utf-8"))
            self.assertTrue((output / OWNERSHIP_MARKER).is_file())
            self.assertEqual([output], list(root.iterdir()))

    def test_staged_output_restores_the_previous_site_if_installation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "site"
            prepare_output(output)
            (output / "index.html").write_text("old", encoding="utf-8")
            original_rename = Path.rename

            def failing_install(path: Path, target: Path):
                if path == staging:
                    raise OSError("installation failed")
                return original_rename(path, target)

            with self.assertRaisesRegex(OSError, "installation failed"), patch.object(Path, "rename", new=failing_install):
                with staged_output(output) as staging:
                    prepare_output(staging)
                    (staging / "index.html").write_text("new", encoding="utf-8")

            self.assertEqual("old", (output / "index.html").read_text(encoding="utf-8"))
            self.assertEqual([output], list(root.iterdir()))

    def test_staged_output_rechecks_ownership_before_publishing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "site"
            with self.assertRaisesRegex(DocSproutError, "not owned"):
                with staged_output(output) as staging:
                    prepare_output(staging)
                    output.mkdir()
                    (output / "important.txt").write_text("keep", encoding="utf-8")

            self.assertEqual("keep", (output / "important.txt").read_text(encoding="utf-8"))
            self.assertEqual([output], list(root.iterdir()))

    def test_refuses_to_replace_an_unowned_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "site"
            output.mkdir()
            (output / "important.txt").write_text("keep", encoding="utf-8")

            with self.assertRaisesRegex(DocSproutError, "not owned"):
                prepare_output(output)

            self.assertEqual("keep", (output / "important.txt").read_text(encoding="utf-8"))

    def test_replaces_a_directory_marked_as_owned(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "site"
            prepare_output(output)
            (output / "old.html").write_text("old", encoding="utf-8")

            prepare_output(output)

            self.assertFalse((output / "old.html").exists())
            self.assertTrue((output / OWNERSHIP_MARKER).exists())

    def test_recognises_and_replaces_the_legacy_ownership_marker(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "site"
            output.mkdir()
            (output / ".dockit-fp-site").write_text("DocKit-FP generated output.\n", encoding="utf-8")
            (output / "old.html").write_text("old", encoding="utf-8")

            prepare_output(output)

            self.assertFalse((output / "old.html").exists())
            self.assertFalse((output / ".dockit-fp-site").exists())
            self.assertTrue((output / OWNERSHIP_MARKER).exists())
