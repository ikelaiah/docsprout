from pathlib import Path
import unittest


class PublishingWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parents[1]

    def test_reusable_workflow_supports_versioned_and_single_version_sites(self) -> None:
        workflow = (self.root / ".github" / "workflows" / "publish-docs.yml").read_text(encoding="utf-8")

        self.assertIn("versioned:", workflow)
        self.assertIn("default: true", workflow)
        self.assertIn("release:", workflow)
        self.assertIn("DOCSPROUT_RELEASE: ${{ inputs.release }}", workflow)
        self.assertIn('docsprout build --release "$DOCSPROUT_RELEASE" --output build/docs-site', workflow)
        self.assertIn("if: inputs.versioned", workflow)
        self.assertIn("if: ${{ ! inputs.versioned }}", workflow)

    def test_reusable_workflow_installs_the_pinned_docsprout_release(self) -> None:
        workflow = (self.root / ".github" / "workflows" / "publish-docs.yml").read_text(encoding="utf-8")

        self.assertIn("git+https://github.com/ikelaiah/docsprout.git@v1.1.6", workflow)
        self.assertNotIn("python -m pip install .", workflow)

    def test_workflows_use_checkout_v7_node_24_major(self) -> None:
        ci = (self.root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        publish = (self.root / ".github" / "workflows" / "publish-docs.yml").read_text(encoding="utf-8")

        self.assertIn("actions/checkout@v7", ci)
        self.assertIn("actions/checkout@v7", publish)

    def test_workflows_use_setup_python_v7_node_24_major(self) -> None:
        ci = (self.root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        publish = (self.root / ".github" / "workflows" / "publish-docs.yml").read_text(encoding="utf-8")

        self.assertIn("actions/setup-python@v7", ci)
        self.assertIn("actions/setup-python@v7", publish)

    def test_publish_workflow_uses_upload_pages_artifact_v5(self) -> None:
        publish = (self.root / ".github" / "workflows" / "publish-docs.yml").read_text(encoding="utf-8")

        self.assertIn("actions/upload-pages-artifact@v5", publish)

    def test_publish_workflow_uses_deploy_pages_v5_node_24_major(self) -> None:
        publish = (self.root / ".github" / "workflows" / "publish-docs.yml").read_text(encoding="utf-8")

        self.assertIn("actions/deploy-pages@v5", publish)

    def test_examples_pin_the_release_and_select_the_intended_mode(self) -> None:
        single = (self.root / "examples" / "single-version" / ".github" / "workflows" / "documentation.yml").read_text(encoding="utf-8")
        historical = (self.root / "examples" / "historical" / ".github" / "workflows" / "documentation.yml").read_text(encoding="utf-8")

        self.assertIn("publish-docs.yml@v1.1.6", single)
        self.assertIn("versioned: false", single)
        self.assertIn("publish-docs.yml@v1.1.6", historical)
        self.assertNotIn("versioned: false", historical)
