"""Qualification: exercise DocSprout as an *installed package*, not source checkout.

Run with the Python interpreter of a virtual environment that had DocSprout
installed from a built wheel or sdist, from a working directory outside the
source tree. Every path used here is a fresh temporary directory, so a passing
run is evidence that the package does not depend on repository-only files.

    python qualification_installed.py --expected-version 1.1.2

The script is deliberately self-contained (stdlib only) so it can be copied or
run from any location without importing anything from the repository.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import json
import os
import socket
from pathlib import Path
import subprocess
import sys
import sysconfig
import tempfile
import time
import urllib.request

import docsprout
from docsprout.github_pages import CANONICAL_WORKFLOW_RELATIVE_PATH, render_workflow

EXPECTED_MODULES = (
    "archive", "assets", "audit", "build", "cli", "config", "discovery", "errors",
    "github_pages", "highlight", "markdown", "models", "safety", "versions",
)


class Failure(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Failure(message)


def run(root: Path, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "docsprout", *arguments, "--root", str(root)],
        cwd=str(root), capture_output=True, text=True, encoding="utf-8", timeout=120,
        check=False,
    )


def require_run(root: Path, *arguments: str) -> str:
    result = run(root, *arguments)
    if result.returncode != 0:
        raise Failure(
            f"docsprout {arguments} exited {result.returncode}:\n{result.stdout}\n{result.stderr}"
        )
    return result.stdout


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def qualify_installation(version: str) -> None:
    package = Path(docsprout.__file__).resolve()
    purelib = Path(sysconfig.get_path("purelib")).resolve()
    require(package.is_relative_to(purelib), f"docsprout is not installed at {purelib}: {package}")
    require(str(package).find("src") == -1 or "site-packages" in package.parts, f"docsprout resolves into a source tree: {package}")
    require(importlib.metadata.version("docsprout") == version, "importlib.metadata version mismatch")
    for name in EXPECTED_MODULES:
        require(importlib.util.find_spec(f"docsprout.{name}") is not None, f"installed package cannot import docsprout.{name}")
    require(importlib.util.find_spec("dockit_fp") is not None, "compatibility shim dockit_fp cannot be imported")
    shim = importlib.import_module("dockit_fp")
    require(shim.__version__ == version, "dockit_fp compatibility shim version mismatch")

    vendor = package.parent / "vendor" / "katex"
    for required in ("katex.min.js", "katex.min.css", "LICENSE", "fonts/KaTeX_Main-Regular.woff2", "fonts/KaTeX_AMS-Regular.woff2"):
        asset = vendor / required
        require(asset.is_file() and asset.stat().st_size > 0, f"bundled KaTeX asset missing or empty: {required}")

    from docsprout import assets
    require(len(assets.SITE_CSS) > 1000 and len(assets.SITE_JS) > 1000 and len(assets.MATH_JS) > 100, "bundled browser assets are unexpectedly small")
    require("prefers-reduced-motion" in assets.SITE_CSS, "site CSS lost its reduced-motion rule")
    require("ArrowDown" in assets.SITE_JS, "site JS lost its search keyboard contract")
    require("docsprout-theme" in assets.SITE_JS and "dockit-fp-theme" in assets.SITE_JS, "site JS lost its theme storage migration")

    version_output = subprocess.run(
        [sys.executable, "-m", "docsprout", "--version"], capture_output=True, text=True, check=False,
    )
    require(version_output.returncode == 0, "python -m docsprout --version failed")
    require(version_output.stdout.strip() == f"docsprout {version}", f"CLI version mismatch: {version_output.stdout!r}")

    legacy_version_output = subprocess.run(
        [sys.executable, "-m", "dockit_fp", "--version"], capture_output=True, text=True, check=False,
    )
    require(legacy_version_output.returncode == 0, "python -m dockit_fp --version failed")
    require(legacy_version_output.stdout.strip() == f"dockit-fp {version}", f"legacy CLI version mismatch: {legacy_version_output.stdout!r}")

    scripts = Path(sysconfig.get_path("scripts"))
    executable = scripts / ("docsprout.exe" if os.name == "nt" else "docsprout")
    require(executable.is_file(), f"console script missing at {executable}")
    script_output = subprocess.run([str(executable), "--version"], capture_output=True, text=True, check=False)
    require(script_output.returncode == 0, "docsprout console script --version failed")
    require(script_output.stdout.strip() == f"docsprout {version}", "console script version mismatch")

    legacy_executable = scripts / ("dockit-fp.exe" if os.name == "nt" else "dockit-fp")
    require(legacy_executable.is_file(), f"deprecated console script missing at {legacy_executable}")
    legacy_script_output = subprocess.run([str(legacy_executable), "--version"], capture_output=True, text=True, check=False)
    require(legacy_script_output.returncode == 0, "dockit-fp console script --version failed")
    require(legacy_script_output.stdout.strip() == f"dockit-fp {version}", "legacy console script version mismatch")

    qualify_new_project()
    qualify_existing_repository()
    qualify_legacy_configuration()
    qualify_git_pages_walkthrough(version)
    qualify_serve()


def qualify_new_project() -> None:
    with tempfile.TemporaryDirectory(prefix="ds-installed-new-") as temporary:
        root = Path(temporary)
        init = require_run(root, "init")
        require("DocSprout is ready." in init and "docs/layout.json" in init, "init did not finish the guided message")
        require((root / "docs" / "docsprout.json").is_file(), "init did not create docsprout.json")
        require((root / "docs" / "layout.json").is_file(), "init did not create layout.json")

        check = require_run(root, "check")
        require("Documentation check passed: 1 section(s), 1 page(s)" in check, f"unexpected check output: {check}")

        audit_output = require_run(root, "audit", "--format", "json")
        report = json.loads(audit_output)
        require(report["schema_version"] == 1 and report["errors"] == 0 and report["warnings"] == 0 and report["pages"] == 1, f"unexpected audit report: {audit_output}")

        build_output = require_run(root, "build", "--output", str(root / "site"))
        require(f"Built 1 page(s) in {root / 'site'}" in build_output, f"unexpected build output: {build_output}")
        site = root / "site"
        for relative, marker in (
            ("index.html", "assets/katex/katex.min.js"),
            (".docsprout-site", "DocSprout generated output"),
            ("search-index.json", '"url": "index.html"'),
            ("release.json", "preview"),
            ("assets/site.css", "--dk-accent"),
            ("assets/site.js", "ArrowDown"),
            ("assets/katex/katex.min.js", "katex"),
        ):
            require((site / relative).is_file(), f"built site missing {relative}")
            require(marker in (site / relative).read_text(encoding="utf-8", errors="replace"), f"{relative} lacks expected content marker")
        katex_fonts = list((site / "assets" / "katex" / "fonts").glob("*.woff2"))
        require(len(katex_fonts) >= 3, f"built site lacks KaTeX fonts ({len(katex_fonts)} found)")
        _require_no_path_leak(site, root)


def qualify_existing_repository() -> None:
    with tempfile.TemporaryDirectory(prefix="ds-installed-existing-") as temporary:
        root = Path(temporary)
        docs = root / "docs"
        (docs / "guides").mkdir(parents=True)
        readme = root / "README.md"
        readme.write_text("# Existing repository\n\n[Guide](docs/guides/deep.md)", encoding="utf-8")
        (docs / "guides" / "deep.md").write_text("# Deep guide\n\n[Back](../../README.md)", encoding="utf-8")
        (docs / "draft.md").write_text("# Draft\n\nDo not publish.", encoding="utf-8")
        (docs / "docsprout.json").write_text(json.dumps({"schema_version": 1, "project": {"name": "Existing"}}), encoding="utf-8")
        (docs / "layout.json").write_text(json.dumps({
            "schema_version": 1, "unlisted": "exclude",
            "home": {"path": "README.md", "source": "root"},
            "navigation": [
                {"title": "Overview", "pages": [{"title": "Overview", "path": "README.md", "source": "root"}]},
                {"title": "Guides", "pages": [{"title": "Deep", "path": "guides/deep.md"}]},
            ],
        }), encoding="utf-8")
        readme_before = readme.read_text(encoding="utf-8")
        layout_before = (docs / "layout.json").read_text(encoding="utf-8")

        init = require_run(root, "init")
        require("left authoritative" in init, "init changed an existing configuration")

        check = require_run(root, "check")
        require("1 unlisted document(s) excluded" in check, f"check did not report the excluded draft: {check}")

        build = require_run(root, "build", "--output", str(root / "site"))
        require("Built 2 page(s)" in build, f"unexpected build output: {build}")
        site = root / "site"
        require("Existing repository" in (site / "index.html").read_text(encoding="utf-8"), "root README was not the home")
        require((site / "guides" / "deep.html").is_file(), "nested guide route missing")
        require((site / "draft.html").exists() is False, "unlisted draft was published")
        require(readme_before == readme.read_text(encoding="utf-8"), "init or build modified the README")
        require(layout_before == (docs / "layout.json").read_text(encoding="utf-8"), "build modified the layout")
        search = json.loads((site / "search-index.json").read_text(encoding="utf-8"))
        require(search["schema_version"] == 1 and [entry["url"] for entry in search["entries"]] == ["index.html", "guides/deep.html"], f"unexpected search index: {search}")
        _require_no_path_leak(site, root)


def qualify_legacy_configuration() -> None:
    with tempfile.TemporaryDirectory(prefix="ds-installed-legacy-") as temporary:
        root = Path(temporary)
        docs = root / "docs"
        docs.mkdir()
        (docs / "index.md").write_text("# Legacy configuration\n", encoding="utf-8")
        (docs / "dockit.json").write_text(json.dumps({"schema_version": 1, "project": {"name": "Legacy"}}), encoding="utf-8")
        (docs / "layout.json").write_text(json.dumps({
            "schema_version": 1,
            "navigation": [{"title": "Docs", "pages": [{"title": "Home", "path": "index.md"}]}],
        }), encoding="utf-8")

        check = require_run(root, "check")
        require("Documentation check passed" in check, f"legacy dockit.json did not load: {check}")

        build = require_run(root, "build", "--output", str(root / "site"))
        require("Built 1 page(s)" in build, f"legacy dockit.json did not build: {build}")
        require((root / "site" / ".docsprout-site").is_file(), "legacy project did not receive the DocSprout ownership marker")


def qualify_git_pages_walkthrough(version: str) -> None:
    with tempfile.TemporaryDirectory(prefix="ds-installed-pages-") as temporary:
        root = Path(temporary)
        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.email", "tests@example.test"], cwd=root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.name", "Tests"], cwd=root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "remote", "add", "origin", "git@github.com:example/installed-pages.git"], cwd=root, check=True, capture_output=True, text=True)
        (root / "README.md").write_text("# Installed pages\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "commit", "-m", "seed"], cwd=root, check=True, capture_output=True, text=True)
        head_before = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True).stdout

        prepared = require_run(root, "github-pages")
        require("DocSprout is ready for GitHub Pages." in prepared, f"unexpected github-pages output: {prepared}")
        workflow = root / CANONICAL_WORKFLOW_RELATIVE_PATH
        require(workflow.is_file(), "github-pages did not create the managed workflow")
        require(workflow.read_text(encoding="utf-8") == render_workflow(f"v{version}"), "managed workflow does not pin the installed release")

        rerun = require_run(root, "github-pages")
        require("No changes required." in rerun, f"second run was not idempotent: {rerun}")
        head_after = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True).stdout
        require(head_before == head_after, "github-pages committed or rewrote Git history")
        log = subprocess.run(["git", "log", "--oneline"], cwd=root, check=True, capture_output=True, text=True).stdout
        require(len(log.splitlines()) == 1, "github-pages created a commit")
        status = subprocess.run(["git", "status", "--porcelain"], cwd=root, check=True, capture_output=True, text=True).stdout
        require("?? docs/" in status and "?? .github/" in status, f"expected only new DocSprout files: {status}")

        workflow.write_text(render_workflow("v0.12.1"), encoding="utf-8")
        told = require_run(root, "github-pages")
        require("--update" in told, "outdated workflow was not reported")
        still = workflow.read_text(encoding="utf-8")
        require(still == render_workflow("v0.12.1"), "github-pages updated without --update")
        updated = require_run(root, "github-pages", "--update")
        require("Updated" in updated, f"--update did not update the workflow: {updated}")
        require(workflow.read_text(encoding="utf-8") == render_workflow(f"v{version}"), "--update did not pin the installed release")


def qualify_serve() -> None:
    with tempfile.TemporaryDirectory(prefix="ds-installed-serve-") as temporary:
        root = Path(temporary)
        require_run(root, "init")
        port = free_port()
        server = subprocess.Popen(
            [sys.executable, "-u", "-m", "docsprout", "serve", "--root", str(root), "--port", str(port)],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        )
        try:
            page = read_with_retries(port)
            require("Welcome to the documentation." in page, "served home page lacks expected content")
            css = read_with_retries(port, "/assets/site.css")
            require("--dk-accent" in css, "served site asset lacks expected CSS")
        finally:
            server.terminate()
            server.wait(timeout=15)
        log = server.stdout.read() if server.stdout else ""
        require("Serving documentation at" in log, f"serve did not announce its URL: {log}")


def _require_no_path_leak(site: Path, root: Path) -> None:
    root_text = str(root)
    for path in site.rglob("*"):
        if not path.is_file():
            continue
        contents = path.read_text(encoding="utf-8", errors="replace")
        require(root_text not in contents, f"built file {path.relative_to(site)} embeds the project path {root_text}")


def read_with_retries(port: int, path: str = "/", attempts: int = 40) -> str:
    url = f"http://127.0.0.1:{port}{path}"
    last_error: Exception | None = None
    for _ in range(attempts):
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                return response.read().decode("utf-8")
        except Exception as error:  # noqa: BLE001 - retry while the server boots
            last_error = error
            time.sleep(0.25)
    raise Failure(f"server never answered {url}: {last_error}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-version", required=True)
    arguments = parser.parse_args()
    try:
        qualify_installation(arguments.expected_version)
    except Failure as failure:
        print(f"Installed-package qualification FAILED for v{arguments.expected_version}: {failure}")
        print(f"Python: {sys.version.split()[0]}; package: {Path(docsprout.__file__).resolve()}")
        return 1
    print(f"Installed-package qualification passed for v{arguments.expected_version}: "
          f"wheel/sdist install, imports, bundled KaTeX assets, console scripts, "
          f"new-project and existing-repository journeys, legacy dockit.json loading, "
          f"github-pages preparation, serve smoke.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
