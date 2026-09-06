from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from dockit_fp.github_pages import MANAGED_MARKER, inspect_workflow, render_workflow


class ManagedGitHubPagesWorkflowTests(unittest.TestCase):
    def test_renders_a_pinned_default_branch_pages_workflow(self) -> None:
        workflow = render_workflow("v0.14.0")

        self.assertIn(MANAGED_MARKER, workflow)
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("github.event.repository.default_branch", workflow)
        self.assertIn("publish-docs.yml@v0.14.0", workflow)
        self.assertIn("versioned: false", workflow)
        self.assertIn("contents: read", workflow)
        self.assertIn("pages: write", workflow)
        self.assertIn("id-token: write", workflow)
        self.assertIn("cancel-in-progress: false", workflow)

    def test_classifies_absent_current_outdated_unmanaged_and_malformed_workflows(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / ".github" / "workflows" / "dockit-pages.yml"

            self.assertEqual("absent", inspect_workflow(path, "v0.14.0").state)
            path.parent.mkdir(parents=True)
            path.write_text(render_workflow("v0.14.0"), encoding="utf-8")
            self.assertEqual("current", inspect_workflow(path, "v0.14.0").state)
            path.write_text(render_workflow("v0.13.0"), encoding="utf-8")
            self.assertEqual("outdated", inspect_workflow(path, "v0.14.0").state)
            path.write_text("name: Personal Pages\n", encoding="utf-8")
            self.assertEqual("unmanaged", inspect_workflow(path, "v0.14.0").state)
            path.write_text(f"{MANAGED_MARKER}\nname: Broken\n", encoding="utf-8")
            self.assertEqual("malformed", inspect_workflow(path, "v0.14.0").state)

    def test_maintained_workflow_fixture_matches_the_template(self) -> None:
        from dockit_fp import __version__
        root = Path(__file__).resolve().parents[1]
        fixture = root / "examples" / "github-pages" / ".github" / "workflows" / "dockit-pages.yml"

        self.assertEqual(render_workflow(f"v{__version__}"), fixture.read_text(encoding="utf-8"))

    def test_refuses_a_symlinked_managed_workflow_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflow = root / ".github" / "workflows" / "dockit-pages.yml"
            workflow.parent.mkdir(parents=True)

            with patch("dockit_fp.github_pages.Path.is_symlink", return_value=True):
                self.assertEqual("unsafe", inspect_workflow(workflow, "v0.14.0").state)
