"""Immutable Git-source version manifests and historical site builds."""

from __future__ import annotations

from dataclasses import dataclass
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile

from .build import build_site
from .config import MANIFEST_FIELDS, VERSION_FIELDS, _reject_unknown_fields
from .errors import DocSproutError
from .safety import prepare_output

MOVING_REFS = {"head", "main", "master", "develop", "development", "latest"}
COMMIT = re.compile(r"^[0-9a-fA-F]{40}$")
RELEASE_NAME = re.compile(r"^[0-9A-Za-z][0-9A-Za-z._-]*$")


def _valid_source_ref(value: str) -> bool:
    if COMMIT.fullmatch(value):
        return True
    forbidden = "~^:?*[\\"
    return bool(
        value
        and not value.startswith("-")
        and not value.startswith("/")
        and not value.endswith(("/", "."))
        and ".." not in value
        and "@{" not in value
        and "//" not in value
        and not any(character.isspace() or character in forbidden for character in value)
    )


@dataclass(frozen=True)
class Version:
    release: str
    source_ref: str


@dataclass(frozen=True)
class VersionManifest:
    current: str
    versions: tuple[Version, ...]


@dataclass(frozen=True)
class BuildAllResult:
    release_count: int
    page_count: int


def load_manifest(root: Path) -> VersionManifest:
    path = root / "docs" / "versions.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise DocSproutError(f"{path}: invalid version manifest: {error}") from error
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise DocSproutError(f"{path}: field 'schema_version' must be 1")
    _reject_unknown_fields(data, MANIFEST_FIELDS, "versions", path)
    current, entries = data.get("current"), data.get("versions")
    if not isinstance(current, str) or not isinstance(entries, list) or not entries:
        raise DocSproutError(f"{path}: fields 'current' and non-empty 'versions' are required")
    versions: list[Version] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or not isinstance(entry.get("release"), str) or not isinstance(entry.get("source_ref"), str):
            raise DocSproutError(f"{path}: versions[{index}] needs string release and source_ref")
        _reject_unknown_fields(entry, VERSION_FIELDS, f"versions[{index}]", path)
        release, source_ref = entry["release"], entry["source_ref"]
        if not RELEASE_NAME.fullmatch(release):
            raise DocSproutError(
                f"{path}: versions[{index}].release must be a safe name using letters, numbers, dots, underscores, or hyphens"
            )
        if not _valid_source_ref(source_ref):
            raise DocSproutError(f"{path}: versions[{index}].source_ref must be a safe tag or full commit SHA")
        versions.append(Version(release, source_ref))
    releases = [entry.release for entry in versions]
    source_refs = [entry.source_ref for entry in versions]
    if len(set(releases)) != len(releases) or len(set(source_refs)) != len(source_refs) or current not in releases:
        raise DocSproutError(f"{path}: releases and source refs must be unique, and releases must include current {current!r}")
    return VersionManifest(current, tuple(versions))


def _run_git(root: Path, *arguments: str, binary: bool = False) -> str | bytes:
    completed = subprocess.run(["git", *arguments], cwd=root, capture_output=True, text=not binary)
    if completed.returncode:
        detail = completed.stderr.decode() if binary else completed.stderr
        raise DocSproutError(f"Git {' '.join(arguments)} failed: {detail.strip()}")
    return completed.stdout


def _is_immutable(root: Path, source_ref: str) -> bool:
    if source_ref.lower() in MOVING_REFS:
        return False
    if COMMIT.fullmatch(source_ref):
        return True
    completed = subprocess.run(["git", "show-ref", "--verify", "--quiet", f"refs/tags/{source_ref}"], cwd=root)
    return completed.returncode == 0


def check_release(root: Path) -> VersionManifest:
    root = root.resolve()
    manifest = load_manifest(root)
    for entry in manifest.versions:
        if entry.source_ref.lower() in MOVING_REFS:
            raise DocSproutError(
                f"docs/versions.json: published release {entry.release!r} must not use moving source_ref {entry.source_ref!r}; use a tag or full commit SHA."
            )
        if not COMMIT.fullmatch(entry.source_ref) and not _is_immutable(root, entry.source_ref):
            raise DocSproutError(
                f"docs/versions.json: source_ref {entry.source_ref!r} for release {entry.release!r} does not exist. "
                f"Create the tag with 'git tag {entry.source_ref}' before publishing."
            )
        try:
            _run_git(root, "rev-parse", "--verify", f"{entry.source_ref}^{{commit}}")
        except DocSproutError as error:
            raise DocSproutError(
                f"Cannot build documentation version {entry.release}: source_ref {entry.source_ref!r} does not resolve to a Git object."
            ) from error
    current = next(entry for entry in manifest.versions if entry.release == manifest.current)
    current_commit = str(_run_git(root, "rev-parse", "--verify", f"{current.source_ref}^{{commit}}")).strip()
    head_commit = str(_run_git(root, "rev-parse", "--verify", "HEAD^{commit}")).strip()
    if current_commit != head_commit:
        raise DocSproutError(
            f"docs/versions.json: current release {current.release!r} source_ref {current.source_ref!r} does not match HEAD. "
            "Tag the commit being published or check out the declared release commit."
        )
    changed_docs = str(_run_git(root, "status", "--porcelain", "--untracked-files=all", "--", "docs")).strip()
    if changed_docs:
        raise DocSproutError("Documentation differs from HEAD. Commit docs changes before publishing the current release.")
    return manifest


def _archive_to(root: Path, source_ref: str, destination: Path) -> None:
    archive = _run_git(root, "archive", "--format=tar", source_ref, binary=True)
    assert isinstance(archive, bytes)
    with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
        for member in bundle.getmembers():
            target = (destination / member.name).resolve()
            if not target.is_relative_to(destination.resolve()):
                raise DocSproutError(f"Git archive contains unsafe path {member.name!r}")
        if sys.version_info >= (3, 12):
            bundle.extractall(destination, filter="data")
        else:
            bundle.extractall(destination)


def build_all(*, root: Path, output: Path) -> BuildAllResult:
    """Build all manifest releases exclusively from their immutable Git source."""
    root = root.resolve()
    manifest = check_release(root)
    output = output.resolve()
    prepare_output(output)
    page_count = 0
    with tempfile.TemporaryDirectory(prefix="docsprout-") as temporary:
        staging = Path(temporary)
        targets = tuple((item.release, f"{item.release}/index.html") for item in manifest.versions)
        for item in manifest.versions:
            source = staging / item.release
            source.mkdir()
            _archive_to(root, item.source_ref, source)
            result = build_site(
                root=source, output=output / item.release, release=item.release, versions=targets,
                require_listed_documents=item.release == manifest.current,
            )
            page_count += result.page_count
    (output / "versions.json").write_text(json.dumps({
        "schema_version": 1, "current": manifest.current,
        "versions": [{"release": item.release, "source_ref": item.source_ref} for item in manifest.versions],
    }, indent=2) + "\n", encoding="utf-8")
    (output / "index.html").write_text(
        f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={manifest.current}/index.html"><a href="{manifest.current}/index.html">Open {manifest.current} documentation</a>\n',
        encoding="utf-8",
    )
    return BuildAllResult(len(manifest.versions), page_count)
