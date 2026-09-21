import unittest
import io
import json
from pathlib import Path
import tempfile
from contextlib import redirect_stdout

from docsprout.cli import main
from docsprout import __version__


def _write_project(root: Path, pages: dict[str, str], *, layout_pages: list[str] | None = None, home: dict | None = None) -> None:
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    for path, content in pages.items():
        target = root / path if path == "README.md" else docs / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    listed = layout_pages if layout_pages is not None else [path for path in pages if path == "README.md" or path.endswith(".md")]
    navigation = [{"title": "Docs", "pages": [
        {"title": Path(path).stem.title(), "path": path, **({"source": "root"} if path == "README.md" else {})}
        for path in listed
    ]}]
    layout: dict[str, object] = {"schema_version": 1, "unlisted": "exclude", "navigation": navigation}
    if home is not None:
        layout["home"] = home
    (docs / "docsprout.json").write_text('{"schema_version": 1, "project": {"name": "Demo"}}', encoding="utf-8")
    (docs / "layout.json").write_text(json.dumps(layout), encoding="utf-8")


class AuditTests(unittest.TestCase):
    def test_intentionally_bad_fixture_exercises_every_audit_rule(self) -> None:
        from docsprout.audit import audit_project

        root = Path(__file__).resolve().parents[1] / "examples" / "audit-fixture"

        findings = audit_project(root).findings

        self.assertEqual(
            ["DK001", "DK002", "DK003", "DK101", "DK004", "DK005", "DK102", "DK103"],
            [finding.code for finding in findings],
        )

    def test_audit_reports_no_findings_for_a_clean_project(self) -> None:
        from docsprout.audit import audit_project

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _write_project(root, {"index.md": "# Home\n\n[Guide](guide.md#install)\n", "guide.md": "# Guide\n\n## Install\n"})

            result = audit_project(root)

        self.assertEqual(2, result.pages)
        self.assertEqual((), result.findings)

    def test_audit_reports_page_anchor_unpublished_asset_and_path_errors(self) -> None:
        from docsprout.audit import audit_project

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _write_project(root, {
                "index.md": "# Home\n\n[Missing](missing.md)\n[Private](private.md)\n[Anchor](guide.md#missing)\n![Diagram](images/nope.svg)\n[Outside](../secret.md)\n",
                "guide.md": "# Guide\n\n## Present\n",
                "private.md": "# Private\n",
            }, layout_pages=["index.md", "guide.md"])

            findings = audit_project(root).findings

        self.assertEqual(["DK001", "DK002", "DK003", "DK004", "DK005"], [finding.code for finding in findings])
        self.assertEqual([3, 4, 5, 6, 7], [finding.line for finding in findings])

    def test_audit_accepts_root_readme_valid_assets_and_non_document_urls(self) -> None:
        from docsprout.audit import audit_project

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _write_project(root, {
                "README.md": "# Project\n\n[Guide](docs/guide.md#install)\n",
                "guide.md": "# Guide\n\n## Install\n\n![Diagram](images/diagram.svg)\n[Mail](mailto:docs@example.test) [Web](https://example.test)\n",
                "images/diagram.svg": "<svg/>",
            }, layout_pages=["README.md", "guide.md"], home={"path": "guide.md"})

            result = audit_project(root)

        self.assertEqual((), result.findings)

    def test_audit_warns_for_empty_image_alt_heading_jump_and_duplicate_anchor(self) -> None:
        from docsprout.audit import audit_project

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _write_project(root, {"index.md": "# Home\n\n![](image.svg)\n\n## One\n\n#### Four\n\n## One\n", "image.svg": "asset"})

            findings = audit_project(root).findings

        self.assertEqual(["DK101", "DK102", "DK103"], [finding.code for finding in findings])

    def test_audit_ignores_markdown_looking_content_in_code_fences(self) -> None:
        from docsprout.audit import audit_project

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _write_project(root, {"index.md": "# Home\n\n```markdown\n[Broken](missing.md)\n![](missing.svg)\n```\n"})

            self.assertEqual((), audit_project(root).findings)

    def test_audit_reports_unsafe_url_schemes_instead_of_treating_them_as_external(self) -> None:
        from docsprout.audit import audit_project

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _write_project(root, {"index.md": "# Home\n\n[Unsafe](javascript:alert(1))\n"})

            findings = audit_project(root).findings

        self.assertEqual("DK005", findings[0].code)

    def test_audit_cli_formats_deterministic_json_and_strict_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _write_project(root, {"index.md": "# Home\n\n![](present.svg)\n", "present.svg": "asset"})
            before = {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(0, main(["audit", "--root", str(root), "--format", "json"]))
            payload = json.loads(output.getvalue())
            with redirect_stdout(io.StringIO()):
                self.assertEqual(1, main(["audit", "--root", str(root), "--strict"]))
            after = {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}

        self.assertEqual({"pages": 1, "errors": 0, "warnings": 1}, {key: payload[key] for key in ("pages", "errors", "warnings")})
        self.assertEqual(1, payload["schema_version"])
        self.assertEqual("DK101", payload["findings"][0]["code"])
        self.assertEqual(before, after)

    def test_audit_returns_usage_failure_for_invalid_configuration_and_version_is_available(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "docs").mkdir()
            (root / "docs" / "docsprout.json").write_text("{}", encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(2, main(["audit", "--root", str(root)]))

        version = io.StringIO()
        with self.assertRaises(SystemExit) as exit_code, redirect_stdout(version):
            main(["--version"])
        self.assertEqual(0, exit_code.exception.code)
        self.assertIn(__version__, version.getvalue())
