"""Conservative, read-only discovery for adopting an existing repository."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit


ANCILLARY_MARKDOWN = ("CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md")


@dataclass(frozen=True)
class RepositoryDiscovery:
    project_name: str
    is_git_repository: bool
    github_remote_url: str | None
    has_readme: bool
    documents: tuple[str, ...]
    ancillary_documents: tuple[str, ...]
    has_docsprout_config: bool
    has_legacy_dockit_config: bool
    has_layout: bool

    @property
    def has_config(self) -> bool:
        """Whether a supported configuration file already exists under docs/."""
        return self.has_docsprout_config or self.has_legacy_dockit_config


def _display_title(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("-", " ").replace("_", " ")).strip().title()


def _github_url(remote: str) -> str | None:
    remote = remote.strip()
    if remote.startswith("git@github.com:"):
        path = remote.removeprefix("git@github.com:")
    else:
        parsed = urlsplit(remote)
        if parsed.hostname != "github.com":
            return None
        path = parsed.path.lstrip("/")
    if not path or "/" not in path:
        return None
    owner, repository = path.removesuffix(".git").split("/", 1)
    if not owner or not repository or "/" in repository:
        return None
    return f"https://github.com/{owner}/{repository}"


def _git_remote(root: Path) -> tuple[bool, str | None]:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"], cwd=root,
            capture_output=True, text=True, check=False,
        )
    except OSError:
        return False, None
    if result.returncode or result.stdout.strip().lower() != "true":
        return False, None
    remote = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"], cwd=root,
        capture_output=True, text=True, check=False,
    )
    return True, _github_url(remote.stdout) if remote.returncode == 0 else None


def discover_repository(root: Path) -> RepositoryDiscovery:
    """Read only the safe default documentation candidates below *root*."""
    root = root.resolve()
    docs = root / "docs"
    is_git_repository, github_remote_url = _git_remote(root)
    def inside_root(path: Path) -> bool:
        try:
            return path.resolve().is_relative_to(root)
        except OSError:
            return False

    documents = tuple(sorted(
        path.relative_to(docs).as_posix() for path in docs.rglob("*.md")
        if path.is_file() and inside_root(path)
    )) if docs.is_dir() else ()
    ancillary = tuple(name for name in ANCILLARY_MARKDOWN if (root / name).is_file() and inside_root(root / name))
    project_name = root.name
    if github_remote_url:
        project_name = github_remote_url.rsplit("/", 1)[-1]
    return RepositoryDiscovery(
        project_name=project_name or "MyLibrary-FP",
        is_git_repository=is_git_repository,
        github_remote_url=github_remote_url,
        has_readme=(root / "README.md").is_file() and inside_root(root / "README.md"),
        documents=documents,
        ancillary_documents=ancillary,
        has_docsprout_config=(docs / "docsprout.json").is_file(),
        has_legacy_dockit_config=(docs / "dockit.json").is_file(),
        has_layout=(docs / "layout.json").is_file(),
    )


def initial_navigation(discovery: RepositoryDiscovery) -> list[dict[str, object]]:
    """Build a deterministic first navigation from only approved candidates."""
    sections: list[dict[str, object]] = []
    if discovery.has_readme:
        sections.append({"title": "Overview", "pages": [
            {"title": "Overview", "path": "README.md", "source": "root"},
        ]})
    grouped: dict[str, list[str]] = {}
    for document in discovery.documents:
        parent = Path(document).parent.as_posix()
        grouped.setdefault(parent, []).append(document)
    for parent in sorted(grouped, key=lambda value: (value == ".", value)):
        title = "Documentation" if parent == "." else _display_title(Path(parent).name)
        pages = [
            {"title": _display_title(Path(document).stem), "path": document}
            for document in sorted(grouped[parent], key=lambda value: (Path(value).stem.lower() != "index", value.lower()))
        ]
        sections.append({"title": title, "pages": pages})
    return sections
