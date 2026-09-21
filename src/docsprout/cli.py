"""The public `docsprout` command-line interface."""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import importlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import threading

from .build import build_site
from . import assets as assets_module
from . import build as build_module
from .audit import audit_project, format_json as format_audit_json, format_text as format_audit_text
from .archive import write_offline_archive
from . import __version__
from .config import CONFIG_FILENAME, load_config, resolve_config_path
from .discovery import discover_repository, initial_navigation
from .errors import DocSproutError
from .github_pages import (
    CANONICAL_WORKFLOW_RELATIVE_PATH,
    LEGACY_WORKFLOW_RELATIVE_PATH,
    inspect_workflow,
    render_workflow,
)
from .versions import build_all, check_release, load_manifest


def _root_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root (default: current directory)")


def _init(root: Path) -> list[str]:
    docs = root / "docs"
    resolve_config_path(docs)
    discovery = discover_repository(root)
    docs.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    if not discovery.has_config:
        project = {"name": discovery.project_name, "description": f"Documentation for {discovery.project_name}"}
        if discovery.github_remote_url:
            project["repository_url"] = discovery.github_remote_url
        (docs / CONFIG_FILENAME).write_text(json.dumps({
            "schema_version": 1, "project": project,
            "theme": {"accent": "#0f766e", "accent_secondary": "#0891b2"},
        }, indent=2) + "\n", encoding="utf-8")
        created.append(f"docs/{CONFIG_FILENAME}")
    navigation = initial_navigation(discovery)
    if not navigation:
        index = docs / "index.md"
        if not index.exists():
            index.write_text(f"# {discovery.project_name}\n\nWelcome to the documentation.\n", encoding="utf-8")
            created.append("docs/index.md")
        navigation = [{"title": "Getting started", "pages": [{"title": "Introduction", "path": "index.md"}]}]
    if not discovery.has_layout:
        pages = [page for section in navigation for page in section["pages"]]
        home = next((page for page in pages if page.get("source") == "root"), None)
        if home is None:
            home = next((page for page in pages if page["path"] == "index.md"), pages[0])
        layout = {"schema_version": 1, "unlisted": "exclude", "home": {key: home[key] for key in ("path", "source") if key in home}, "navigation": navigation}
        (docs / "layout.json").write_text(json.dumps(layout, indent=2) + "\n", encoding="utf-8")
        created.append("docs/layout.json")
    detected = ["Git repository" if discovery.is_git_repository else "non-Git project"]
    if discovery.github_remote_url:
        detected.append(f"GitHub remote {discovery.github_remote_url}")
    if discovery.has_readme:
        detected.append("root README.md")
    if discovery.documents:
        detected.append(f"{len(discovery.documents)} Markdown document(s) under docs/")
    if discovery.has_config or discovery.has_layout:
        detected.append("existing DocSprout configuration")
    messages = [f"Initialised {docs}", f"Detected: {', '.join(detected)}."]
    if created:
        messages.append(f"Created: {', '.join(created)}.")
    else:
        messages.append("Existing DocSprout configuration was left authoritative; no files were changed.")
    messages.append("Published automatically: README.md and Markdown under docs/ only.")
    if discovery.ancillary_documents:
        messages.append(f"Available for explicit inclusion: {', '.join(discovery.ancillary_documents)}.")
    messages.append("Existing Markdown was left untouched.")
    if not discovery.has_layout and navigation:
        sections = ", ".join(
            f"{section['title']} ({len(section['pages'])} page{'s' if len(section['pages']) != 1 else ''})"
            for section in navigation
        )
        messages.append(f"Navigation sections: {sections}.")
    messages.extend((
        "DocSprout is ready.",
        "  Write documentation: README.md and docs/*.md",
        "  Add, rename, group or reorder pages:  docs/layout.json",
        f"  Change colours, logo and presentation:  docs/{CONFIG_FILENAME}",
        "  Preview:  docsprout serve",
    ))
    return messages


def _check(root: Path):
    with tempfile.TemporaryDirectory(prefix="docsprout-check-") as temporary:
        result = build_site(root=root, output=Path(temporary) / "site", release="preview")
    return result


def _github_pages(root: Path, *, update: bool) -> list[str]:
    """Prepare only DocSprout-owned configuration and its Pages caller workflow."""
    discovery = discover_repository(root)
    if not discovery.is_git_repository:
        raise DocSproutError(
            "github-pages: this folder is not a Git repository. Run the command from a repository you plan to push to GitHub."
        )
    version = f"v{__version__}"
    canonical_path = root / CANONICAL_WORKFLOW_RELATIVE_PATH
    legacy_path = root / LEGACY_WORKFLOW_RELATIVE_PATH
    canonical = inspect_workflow(canonical_path, version)
    legacy = inspect_workflow(legacy_path, version)
    for inspection in (canonical, legacy):
        if inspection.state == "unsafe":
            raise DocSproutError(
                f"{inspection.path} contains a symlinked path component. Use a regular repository-local path; no files were changed."
            )
    if canonical.state != "absent" and legacy.state != "absent":
        raise DocSproutError(
            f"Both {CANONICAL_WORKFLOW_RELATIVE_PATH} and {LEGACY_WORKFLOW_RELATIVE_PATH} exist. "
            "DocSprout will not create a second deployment workflow: keep the canonical "
            f"{CANONICAL_WORKFLOW_RELATIVE_PATH} and remove {LEGACY_WORKFLOW_RELATIVE_PATH}."
        )
    if canonical.state == "unmanaged":
        raise DocSproutError(
            f"{CANONICAL_WORKFLOW_RELATIVE_PATH} already exists and is not managed by DocSprout. No files were changed."
        )
    if canonical.state == "malformed":
        raise DocSproutError(
            f"{CANONICAL_WORKFLOW_RELATIVE_PATH} is marked as DocSprout-managed but is malformed. Repair it manually; no files were changed."
        )
    if legacy.state == "unmanaged":
        raise DocSproutError(
            f"{LEGACY_WORKFLOW_RELATIVE_PATH} already exists and is not managed by DocSprout. "
            f"DocSprout will not overwrite it or create {CANONICAL_WORKFLOW_RELATIVE_PATH} alongside it. "
            "Remove or rename it first; no files were changed."
        )
    if legacy.state == "malformed":
        raise DocSproutError(
            f"{LEGACY_WORKFLOW_RELATIVE_PATH} is marked as DocSprout-managed but is malformed. Repair it manually; no files were changed."
        )
    if canonical.state != "absent":
        workflow, inspection = canonical_path, canonical
    elif legacy.state != "absent":
        workflow, inspection = legacy_path, legacy
    else:
        workflow, inspection = canonical_path, canonical
    relative_workflow = workflow.relative_to(root).as_posix()
    if update:
        if inspection.state == "absent":
            raise DocSproutError(f"{CANONICAL_WORKFLOW_RELATIVE_PATH} does not exist. Run 'docsprout github-pages' first.")
        if inspection.state == "current":
            return ["GitHub Pages workflow is already current. No changes required."]
        workflow.write_text(render_workflow(version), encoding="utf-8")
        messages = [f"Updated {relative_workflow} from {inspection.version} to {version}."]
        if workflow == legacy_path:
            messages.append(f"Kept the existing managed path; new projects use {CANONICAL_WORKFLOW_RELATIVE_PATH}.")
        return messages
    if inspection.state == "outdated":
        return [
            f"{relative_workflow} is managed by DocSprout but uses {inspection.version}; current DocSprout is {version}.",
            "Run 'docsprout github-pages --update' to update only that workflow.",
        ]
    if discovery.has_config or discovery.has_layout:
        try:
            load_config(root)
        except DocSproutError as error:
            raise DocSproutError(f"github-pages: existing DocSprout configuration is invalid: {error}. No files were changed.") from error
    initialisation = _init(root)
    result = _check(root)
    if inspection.state == "absent":
        workflow.parent.mkdir(parents=True, exist_ok=True)
        workflow.write_text(render_workflow(version), encoding="utf-8")
    created = next((message for message in initialisation if message.startswith("Created:")), None)
    messages = ["DocSprout is ready for GitHub Pages."]
    if created:
        messages.extend((created, f"Created: {relative_workflow}."))
    else:
        messages.append("No changes required.")
    messages.append(f"Home: {result.home_document}")
    if discovery.github_remote_url:
        messages.append(f"GitHub remote: {discovery.github_remote_url}")
    else:
        messages.append("GitHub remote: not connected to GitHub yet; add a remote before pushing.")
    messages.extend(("Next:", "  git add .", '  git commit -m "Add DocSprout documentation"', "  git push"))
    return messages


class _PreviewBuilder:
    """Rebuild a local preview when its documentation sources change."""

    def __init__(
        self, *, root: Path, output: Path, release: str, renderer_sources: tuple[Path, ...] | None = None,
    ) -> None:
        self.root = root.resolve()
        self.output = output.resolve()
        self.release = release
        self._snapshot: tuple[tuple[str, int, int], ...] = ()
        package = Path(__file__).resolve().parent
        self._renderer_sources = tuple(
            path.resolve()
            for path in (renderer_sources if renderer_sources is not None else (package / "assets.py", package / "build.py"))
        )
        self._renderer_snapshot: tuple[tuple[str, int, int], ...] = ()
        self._lock = threading.Lock()

    def _source_snapshot(self) -> tuple[tuple[str, int, int], ...]:
        sources: list[Path] = []
        readme = self.root / "README.md"
        if readme.is_file():
            sources.append(readme)
        docs = self.root / "docs"
        if docs.is_dir():
            sources.extend(path for path in docs.rglob("*") if path.is_file())
        return tuple(
            (path.relative_to(self.root).as_posix(), path.stat().st_mtime_ns, path.stat().st_size)
            for path in sorted(sources)
        )

    def _renderer_source_snapshot(self) -> tuple[tuple[str, int, int], ...]:
        return tuple(
            (path.as_posix(), path.stat().st_mtime_ns, path.stat().st_size)
            for path in self._renderer_sources if path.is_file()
        )

    @staticmethod
    def _reload_renderer() -> None:
        importlib.reload(assets_module)
        importlib.reload(build_module)

    def build_initial(self) -> None:
        with self._lock:
            build_module.build_site(root=self.root, output=self.output, release=self.release)
            self._snapshot = self._source_snapshot()
            self._renderer_snapshot = self._renderer_source_snapshot()

    def rebuild_if_changed(self) -> bool:
        with self._lock:
            snapshot = self._source_snapshot()
            renderer_snapshot = self._renderer_source_snapshot()
            if snapshot == self._snapshot and renderer_snapshot == self._renderer_snapshot:
                return False
            if renderer_snapshot != self._renderer_snapshot:
                self._reload_renderer()
            try:
                build_module.build_site(root=self.root, output=self.output, release=self.release)
            except DocSproutError:
                self._snapshot = snapshot
                self._renderer_snapshot = renderer_snapshot
                raise
            self._snapshot = self._source_snapshot()
            self._renderer_snapshot = self._renderer_source_snapshot()
            return True


class _PreviewRequestHandler(SimpleHTTPRequestHandler):
    """Serve a preview without allowing a browser cache to hide rebuilds."""

    def __init__(self, *args, preview: _PreviewBuilder, **kwargs) -> None:
        self._preview = preview
        super().__init__(*args, **kwargs)

    def _rebuild_if_needed(self) -> None:
        try:
            if self._preview.rebuild_if_changed():
                print("Rebuilt documentation preview.")
        except DocSproutError as error:
            print(f"Preview rebuild failed: {error}")

    def do_GET(self) -> None:
        self._rebuild_if_needed()
        super().do_GET()

    def do_HEAD(self) -> None:
        self._rebuild_if_needed()
        super().do_HEAD()

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()


def _watch_preview(preview: _PreviewBuilder, stopped: threading.Event) -> None:
    while not stopped.wait(0.25):
        try:
            if preview.rebuild_if_changed():
                print("Rebuilt documentation preview.")
        except DocSproutError as error:
            print(f"Preview rebuild failed: {error}")


def _serve(root: Path, host: str, port: int) -> None:
    """Validate, build, and run a local-only documentation preview server."""
    _check(root)
    output = root / "build" / "docs-site"
    release = load_manifest(root).current if (root / "docs" / "versions.json").exists() else "preview"
    preview = _PreviewBuilder(root=root, output=output, release=release)
    preview.build_initial()
    handler = partial(_PreviewRequestHandler, directory=str(output), preview=preview)
    server = ThreadingHTTPServer((host, port), handler)
    stopped = threading.Event()
    watcher = threading.Thread(target=_watch_preview, args=(preview, stopped), daemon=True)
    watcher.start()
    print(f"Serving documentation at http://{host}:{port}/")
    print("Watching documentation files for changes.")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopped documentation server.")
    finally:
        stopped.set()
        watcher.join(timeout=1)
        server.server_close()


def _doctor(root: Path) -> list[str]:
    messages = [f"Project root: {root}"]
    if not (root / "docs").is_dir():
        return [*messages, "ERROR: docs directory is missing"]
    try:
        config = load_config(root)
        messages.append(f"Documentation: {'legacy discovery' if config.legacy else 'modern configuration'} ({len(config.pages)} page(s))")
    except DocSproutError as error:
        messages.append(f"ERROR: {error}")
    if (root / "docs" / "versions.json").exists():
        try:
            manifest = load_manifest(root)
            messages.append(f"Versions: {len(manifest.versions)} declared; current {manifest.current}")
            messages.append("Status: versioned release configured")
            if shutil.which("git") is None:
                messages.append("ERROR: Git is required for build-all")
            else:
                try:
                    check_release(root)
                    current = next(entry for entry in manifest.versions if entry.release == manifest.current)
                    messages.append(f"Release refs: verified; current {current.source_ref} matches HEAD")
                    messages.append("Next: follow the pre-publish checklist before publishing.")
                except DocSproutError as error:
                    messages.append(f"ERROR: Release refs: {error}")
        except DocSproutError as error:
            messages.append(f"ERROR: {error}")
    else:
        messages.append("Versions: no versions.json (single-release preview only)")
        messages.append("Status: preview-ready")
        messages.append("Next: run docsprout serve.")
    canonical_workflow = inspect_workflow(root / CANONICAL_WORKFLOW_RELATIVE_PATH, f"v{__version__}")
    if canonical_workflow.state != "absent":
        managed, workflow_path = canonical_workflow, CANONICAL_WORKFLOW_RELATIVE_PATH
    else:
        managed, workflow_path = inspect_workflow(root / LEGACY_WORKFLOW_RELATIVE_PATH, f"v{__version__}"), LEGACY_WORKFLOW_RELATIVE_PATH
    if managed.state == "current":
        messages.append(f"GitHub Pages workflow: configured; DocSprout version: {managed.version}")
        if workflow_path == LEGACY_WORKFLOW_RELATIVE_PATH:
            messages.append(
                f"Note: {workflow_path} is the pre-rebrand managed path; new projects use {CANONICAL_WORKFLOW_RELATIVE_PATH}."
            )
    elif managed.state == "outdated":
        messages.append(f"GitHub Pages workflow: update available ({managed.version} → v{__version__}); run docsprout github-pages --update")
    elif managed.state == "unmanaged":
        messages.append(f"WARNING: {workflow_path} is not managed by DocSprout")
    elif managed.state == "malformed":
        messages.append(f"WARNING: {workflow_path} is marked DocSprout-managed but malformed")
    elif managed.state == "unsafe":
        messages.append(f"WARNING: {workflow_path} contains a symlinked path component")
    else:
        workflows = sorted((root / ".github" / "workflows").glob("*.y*ml"))
        workflow_text = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in workflows)
        if "publish-docs.yml@" in workflow_text or "./.github/workflows/publish-docs.yml" in workflow_text:
            mode = "single-version" if "versioned: false" in workflow_text else "historical"
            messages.append(f"Pages: DocSprout {mode} workflow detected")
            if "publish-docs.yml@main" in workflow_text:
                messages.append("WARNING: Pages workflow uses moving ref @main; pin a released DocSprout tag.")
        else:
            messages.append("Pages: no DocSprout workflow detected; see the GitHub Pages guide.")
    return messages


def main(argv: list[str] | None = None, *, prog: str = "docsprout") -> int:
    parser = argparse.ArgumentParser(prog=prog, description="Build offline-friendly Markdown documentation sites for code projects.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (("build", "build current documentation"), ("build-all", "build every immutable release"), ("check", "validate documentation"), ("audit", "report publication-readiness diagnostics"), ("check-release", "validate release refs"), ("init", "adopt or create documentation safely"), ("serve", "validate, build, and preview documentation locally"), ("github-pages", "prepare safe GitHub Pages deployment"), ("doctor", "diagnose project setup")):
        command = commands.add_parser(name, help=help_text)
        _root_argument(command)
        if name == "build":
            command.add_argument("--output", type=Path, help="Output directory (default: build/docs-site)")
            command.add_argument("--release", help="Display release (default: manifest current or preview)")
            command.add_argument("--offline-archive", type=Path, help="Also write a deterministic offline ZIP")
        if name == "build-all":
            command.add_argument("--output", type=Path, help="Output directory (default: build/docs-site)")
        if name == "serve":
            command.add_argument("--host", default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
            command.add_argument("--port", type=int, default=8000, help="Port number (default: 8000)")
        if name == "github-pages":
            command.add_argument("--update", action="store_true", help="Update only a recognised managed Pages workflow")
        if name == "audit":
            command.add_argument("--strict", action="store_true", help="Treat warnings as a failing audit")
            command.add_argument("--format", choices=("text", "json"), default="text", help="Output format (default: text)")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "init":
            print("\n".join(_init(root)))
        elif args.command == "build":
            release = args.release
            if release is None and (root / "docs" / "versions.json").exists():
                release = load_manifest(root).current
            output = args.output or root / "build" / "docs-site"
            result = build_site(root=root, output=output, release=release or "preview")
            if args.offline_archive:
                write_offline_archive(output, args.offline_archive, release or "preview")
            print(f"Built {result.page_count} page(s) in {output}")
        elif args.command == "build-all":
            output = args.output or root / "build" / "docs-site"
            result = build_all(root=root, output=output)
            print(f"Built {result.release_count} release(s), {result.page_count} page(s) total")
        elif args.command == "check":
            result = _check(root)
            excluded = f"; {result.excluded_count} unlisted document(s) excluded" if result.excluded_count else ""
            print(f"Documentation check passed: {result.section_count} section(s), {result.page_count} page(s){excluded}")
        elif args.command == "audit":
            result = audit_project(root)
            print(format_audit_json(result) if args.format == "json" else format_audit_text(result))
            return 1 if result.errors or (args.strict and result.warnings) else 0
        elif args.command == "serve":
            if not 1 <= args.port <= 65535:
                raise DocSproutError("serve: port must be between 1 and 65535")
            _serve(root, args.host, args.port)
        elif args.command == "github-pages":
            print("\n".join(_github_pages(root, update=args.update)))
        elif args.command == "check-release":
            manifest = check_release(root)
            print(f"Release check passed: {len(manifest.versions)} immutable release(s)")
        else:
            messages = _doctor(root)
            print("\n".join(messages))
            return 1 if any(message.startswith("ERROR:") for message in messages) else 0
    except DocSproutError as error:
        print(f"{prog}: {error}")
        return 2 if args.command == "audit" else 1
    return 0


def main_dockit_fp() -> int:
    """Console-script entry point for the deprecated ``dockit-fp`` alias."""
    print("dockit-fp: deprecated command; use 'docsprout' instead.", file=sys.stderr)
    return main(prog="dockit-fp")
