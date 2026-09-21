from pathlib import Path
import tempfile
import unittest
import zipfile

from docsprout.archive import write_offline_archive


class OfflineArchiveTests(unittest.TestCase):
    def test_writes_deterministic_zip_and_sha256(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "site"
            root.mkdir()
            (root / "index.html").write_text("Hello", encoding="utf-8")
            archive = Path(temporary) / "docs.zip"

            digest = write_offline_archive(root, archive, "1.0.0")

            self.assertEqual(64, len(digest))
            self.assertIn(digest, archive.with_suffix(".zip.sha256").read_text(encoding="ascii"))
            with zipfile.ZipFile(archive) as bundle:
                self.assertEqual(["docsprout-docs-1.0.0/index.html"], bundle.namelist())
