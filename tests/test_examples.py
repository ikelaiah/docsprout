import io
from contextlib import redirect_stdout
from pathlib import Path
import tempfile
import unittest

from docsprout.build import build_site
from docsprout.cli import main


class ReleaseExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.examples = Path(__file__).resolve().parents[1] / "examples"

    def test_single_version_example_builds_at_the_site_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "site"
            result = build_site(root=self.examples / "single-version", output=output, release="latest")

            self.assertEqual(1, result.page_count)
            self.assertTrue((output / "index.html").exists())
            self.assertFalse((output / "latest").exists())
            self.assertIn('data-visual-theme="paper"', (output / "index.html").read_text(encoding="utf-8"))

    def test_doctor_recognises_the_single_version_pages_workflow(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            self.assertEqual(0, main(["doctor", "--root", str(self.examples / "single-version")]))

        self.assertIn("Status: preview-ready", output.getvalue())
        self.assertIn("Pages: DocSprout single-version workflow detected", output.getvalue())
